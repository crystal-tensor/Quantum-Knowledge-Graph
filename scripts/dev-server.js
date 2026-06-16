const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const { spawn } = require("node:child_process");

const ROOT = path.resolve(__dirname, "..");
const FRONTEND_HOST = "127.0.0.1";
const FRONTEND_START_PORT = Number(process.env.PORT || 6122);
const BACKEND_HOST = "127.0.0.1";
const BACKEND_PORT = Number(process.env.BACKEND_PORT || 6123);
const BACKEND_URL = `http://${BACKEND_HOST}:${BACKEND_PORT}`;

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8"
};

let backendProcess = null;

function requestBackend(pathname = "/api/health", timeoutMs = 1200) {
  return new Promise((resolve) => {
    const req = http.get(`${BACKEND_URL}${pathname}`, { timeout: timeoutMs }, (res) => {
      res.resume();
      res.on("end", () => resolve(res.statusCode >= 200 && res.statusCode < 500));
    });
    req.on("timeout", () => {
      req.destroy();
      resolve(false);
    });
    req.on("error", () => resolve(false));
  });
}

function requestBackendHealth(timeoutMs = 1200) {
  return new Promise((resolve) => {
    const req = http.get(`${BACKEND_URL}/api/health`, { timeout: timeoutMs }, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => { body += chunk; });
      res.on("end", () => {
        if (res.statusCode < 200 || res.statusCode >= 500) {
          resolve(null);
          return;
        }
        try {
          resolve(JSON.parse(body));
        } catch {
          resolve(null);
        }
      });
    });
    req.on("timeout", () => {
      req.destroy();
      resolve(null);
    });
    req.on("error", () => resolve(null));
  });
}

async function ensureBackend() {
  const existingHealth = await requestBackendHealth();
  if (existingHealth) {
    if (existingHealth.base_dir === ROOT) {
      console.log(`[dev] using existing backend at ${BACKEND_URL}`);
      return;
    }
    throw new Error(
      `port ${BACKEND_PORT} is occupied by a different backend (${existingHealth.base_dir || "unknown base_dir"}); stop it and rerun npm run dev`
    );
  }

  console.log("[dev] starting FastAPI backend: python3 reasoning_server.py");
  backendProcess = spawn("python3", ["reasoning_server.py"], {
    cwd: ROOT,
    stdio: "inherit",
    env: process.env
  });

  for (let i = 0; i < 30; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    if (await requestBackend()) {
      console.log(`[dev] backend ready at ${BACKEND_URL}`);
      return;
    }
  }

  throw new Error(`backend did not become ready at ${BACKEND_URL}`);
}

function safeFilePath(urlPath) {
  const cleanPath = decodeURIComponent(urlPath.split("?")[0]);
  const requested = cleanPath === "/" ? "/quantum_reasoning.html" : cleanPath;
  const fullPath = path.normalize(path.join(ROOT, requested));
  if (!fullPath.startsWith(ROOT + path.sep) && fullPath !== ROOT) {
    return null;
  }
  return fullPath;
}

function proxyApi(req, res) {
  const target = new URL(req.url, BACKEND_URL);
  const proxyReq = http.request(
    target,
    {
      method: req.method,
      headers: {
        ...req.headers,
        host: `${BACKEND_HOST}:${BACKEND_PORT}`
      }
    },
    (proxyRes) => {
      res.writeHead(proxyRes.statusCode || 502, proxyRes.headers);
      proxyRes.pipe(res);
    }
  );

  proxyReq.on("error", (err) => {
    res.writeHead(502, { "content-type": "application/json; charset=utf-8" });
    res.end(JSON.stringify({ detail: `Backend proxy failed: ${err.message}` }));
  });

  req.pipe(proxyReq);
}

function serveStatic(req, res) {
  const url = new URL(req.url, `http://${req.headers.host || "localhost"}`);
  if (url.pathname === "/") {
    res.writeHead(302, { location: "/quantum_reasoning.html" });
    res.end();
    return;
  }

  const filePath = safeFilePath(url.pathname);
  if (!filePath) {
    res.writeHead(403, { "content-type": "text/plain; charset=utf-8" });
    res.end("Forbidden");
    return;
  }

  fs.stat(filePath, (statErr, stat) => {
    if (statErr || !stat.isFile()) {
      res.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
      res.end("Not found");
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      "content-type": MIME_TYPES[ext] || "application/octet-stream",
      "cache-control": "no-store"
    });
    fs.createReadStream(filePath).pipe(res);
  });
}

function createServer() {
  return http.createServer((req, res) => {
    if (req.url.startsWith("/api/")) {
      proxyApi(req, res);
      return;
    }
    serveStatic(req, res);
  });
}

function listenOnAvailablePort(startPort) {
  return new Promise((resolve, reject) => {
    const tryPort = (port) => {
      const server = createServer();
      server.on("error", (err) => {
        if (err.code === "EADDRINUSE") {
          tryPort(port + 1);
          return;
        }
        reject(err);
      });
      server.listen(port, FRONTEND_HOST, () => resolve({ server, port }));
    };
    tryPort(startPort);
  });
}

function shutdown() {
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill("SIGTERM");
  }
  process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

(async () => {
  await ensureBackend();
  const { port } = await listenOnAvailablePort(FRONTEND_START_PORT);
  console.log(`[dev] frontend ready: http://${FRONTEND_HOST}:${port}/quantum_reasoning.html`);
  console.log("[dev] press Ctrl+C to stop");
})().catch((err) => {
  console.error(`[dev] ${err.message}`);
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill("SIGTERM");
  }
  process.exit(1);
});

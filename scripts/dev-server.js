const http = require("node:http");
const path = require("node:path");
const { spawn } = require("node:child_process");

const ROOT = path.resolve(__dirname, "..");
const HOST = process.env.HOST || "0.0.0.0";
const PORT = Number(process.env.PORT || 6122);
const PYTHON = process.env.PYTHON || "python3";
const HEALTH_URL = `http://127.0.0.1:${PORT}/api/health`;

let serverProcess = null;

function requestHealth(timeoutMs = 1200) {
  return new Promise((resolve) => {
    const req = http.get(HEALTH_URL, { timeout: timeoutMs }, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => {
        body += chunk;
      });
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

async function waitForServer() {
  for (let i = 0; i < 40; i += 1) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    const health = await requestHealth();
    if (health && health.base_dir === ROOT) {
      return health;
    }
  }
  throw new Error(`service did not become ready at ${HEALTH_URL}`);
}

async function ensureServer() {
  const existingHealth = await requestHealth();
  if (existingHealth) {
    if (existingHealth.base_dir === ROOT) {
      console.log(`[dev] using existing unified service at http://127.0.0.1:${PORT}`);
      return existingHealth;
    }
    throw new Error(
      `port ${PORT} is occupied by another service (${existingHealth.base_dir || "unknown base_dir"}); stop it and rerun npm run dev`
    );
  }

  console.log(`[dev] starting unified FastAPI service on ${HOST}:${PORT}`);
  console.log(`[dev] python: ${PYTHON}`);
  serverProcess = spawn(PYTHON, ["reasoning_server.py"], {
    cwd: ROOT,
    stdio: "inherit",
    env: {
      ...process.env,
      HOST,
      PORT: String(PORT),
    },
  });

  return waitForServer();
}

function shutdown() {
  if (serverProcess && !serverProcess.killed) {
    serverProcess.kill("SIGTERM");
  }
  process.exit(0);
}

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

(async () => {
  await ensureServer();
  console.log(`[dev] app ready: http://127.0.0.1:${PORT}/quantum_reasoning.html`);
  console.log(`[dev] cloud entry: http://8.153.83.178:${PORT}`);
  console.log("[dev] page and /api/* are served from the same port");
  console.log("[dev] press Ctrl+C to stop");

  if (!serverProcess) {
    setInterval(() => {}, 1 << 30);
  }
})().catch((err) => {
  console.error(`[dev] ${err.message}`);
  if (serverProcess && !serverProcess.killed) {
    serverProcess.kill("SIGTERM");
  }
  process.exit(1);
});

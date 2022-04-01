const app = require("express")();
const ProxyChain = require("proxy-chain");

const PORT = process.env.PORT || 8080;
const Proxy = "http://rynym:aNaPEHnJDW4gma4u@54.81.215.168:31112";

app.get("/generate-proxy", async (req, res, next) => {
  try {
    const StaticProxy = await ProxyChain.anonymizeProxy(Proxy);
    console.log(StaticProxy);
    res.status(200).send(StaticProxy.split("//")[1]);
  } catch (e) {
    res.status(500).send(e);
  }
});

app.listen(PORT, () => {
  console.log(`Proxy-Server listening to http://127.0.0.1:${PORT}/`);
});

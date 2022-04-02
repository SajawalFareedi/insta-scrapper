const app = require("express")();
const ProxyChain = require("proxy-chain");

const PORT = process.env.PORT || 8080;
const Proxy = "http://rynym:aNaPEHnJDW4gma4u@proxy.packetstream.io:31112";
const Proxy2 = "http://kuetxqpq-rotate:dwcgpcu5fdwv@p.webshare.io:9999";

app.get("/generate-proxy", async (req, res, next) => {
  try {
    const StaticProxy = await ProxyChain.anonymizeProxy(Proxy || Proxy2);
    console.log(StaticProxy);
    res.status(200).send(StaticProxy.split("//")[1]);
  } catch (e) {
    res.status(500).send(e);
  }
});

app.listen(PORT, () => {
  console.log(`Proxy-Server listening to http://127.0.0.1:${PORT}/`);
});

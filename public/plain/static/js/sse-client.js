function sse(subscribe) {

  var source = new EventSource(subscribe, { withCredentials: true });

  source.onopen = function (event) {
    console.log("[SSE]: SSE Started...");
    console.log("Ping from client.");
  }

  // For `event: site`
  source.addEventListener("site", (event) => {
    window.console.log(`${event.data} from server.`);
  })
  // Ping from client.
  // Pong from server.

  // For `event: close`.
  source.addEventListener("close", (event) => {
    console.log("[SSE]: Close SSE...");
    source.close();
  })
  // For `event: message`
  source.addEventListener("message", (event) => {
    const type = event.type;
    window.console.log(`Data:\r\n${event.data}\r\nWith type: ${type}`);
  })

  // For `event: dependency`
  source.addEventListener("dependency", (event) => {
    const type = event.type;
    // window.console.log(``);
  })

  return source;
}


const TinyUI = {
  // Config.
  sse: sse(subscribe="/subscribe"),
  status: "off",

};



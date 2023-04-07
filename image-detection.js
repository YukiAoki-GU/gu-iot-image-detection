module.exports = function(RED) {
    function PythonShellNode(config) {
        RED.nodes.createNode(this,config);

        var node = this;
        node.on("input", function(msg) {
            try {
                var {PythonShell} = require("../.node-red/node_modules/python-shell"); 
                let options = {
                    pythonPath: "/usr/bin/python3"
                  };
                  PythonShell.run('image-detection.py', null, function (err, result) {
                   if (err) {
                        msg.payload = err;
                    } else {
                        if (result.length > 0) {
                            msg.payload = result;
                        } else {
                            msg.payload = "";
                        }
                    }
                    node.send(msg);
                });
            } catch(err) {
                node.error(err.message);
            }
        });
    }
    RED.nodes.registerType("画像検出",PythonShellNode);
}

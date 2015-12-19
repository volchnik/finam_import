var http = require('http');
var fs = require('fs');

var file = fs.createWriteStream("icharts.js");
var request = http.get("http://www.finam.ru/cache/icharts/icharts.js", function(response) {
  response.pipe(file);
  file.on('finish', function(){
    fs.appendFileSync('icharts.js', "exports.aEmitentCodes = aEmitentCodes; exports.aEmitentIds = aEmitentIds;exports.aEmitentMarkets = aEmitentMarkets;", encoding='utf8');
    
    var chartsData = require('./icharts.js');
    var jsonEmitentIdsString = JSON.stringify(chartsData);

    fs.writeFile("icharts.json", jsonEmitentIdsString, function(err) {
        if(err) {
            return console.log(err);
        }
        console.log("The file was saved!");
    });
  });
});


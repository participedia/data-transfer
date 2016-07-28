var fs = require('fs');
var Converter = require("csvtojson").Converter;
var converter = new Converter({});
converter.transform=function(json,row,index){
  for (key in json) {
    // convert dates to Dates
    // console.log(key);
    if (key.toLowerCase().indexOf('date') != -1) {
      // console.log(key, json[key]);
      if (json[key] == '0') {
        json[key] = undefined;
      } else {
        json[key] = new Date(json[key])
      }
      // console.log(key, json[key]);
    }
    // Would be good to know which columns are booleans, numbers.
  }
  // process.exit(0);
  json["dateOfBirth"]=new Date(json["dateOfBirth"]); // convert a field type
};

all = {}

// converter.fromFile("./methods.csv",function(err,result){
//   var fd = fs.openSync("methods.json", "w")
//   fs.writeSync(fd, JSON.stringify({'methods':result}));
// });
// converter.fromFile("./cases.csv",function(err,result){
//   var fd = fs.openSync("newcases.json", "w")
//   fs.writeSync(fd, JSON.stringify({'cases':result}));
// });
//
converter.fromFile("./organizations.csv",function(err,result){
  var fd = fs.openSync("organizations.json", "w")
  fs.writeSync(fd, JSON.stringify({'organizations':result}));
});

//
//
// converter.fromFile("./newcases.csv",function(err,result){
//   all['cases'] = result;
//   console.log("ERR", err);
//   console.log(JSON.stringify(result).substring(0,100));
// });
// converter.fromFile("./methods.csv",function(err,result){
//   all['methods'] = result;
//   console.log("ERR", err);
//   console.log(JSON.stringify(result).substring(0,100));
// });
// converter.fromFile("./organizations.csv",function(err,result){
//   all['organizations'] = result;
//   console.log("ERR", err);
//   console.log(JSON.stringify(result).substring(0,100));
// });
// //

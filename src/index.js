import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

/*var exec = require('child_process').exec;
function execute(command, callback){
    exec(command, function(error, stdout, stderr){ callback(stdout); });
};
execute("ls", function(res){
  console.log(res);
}); */
console.log("Hello");

ReactDOM.render(
  <App />,
  document.getElementById('root')
);

// import {requirejs} from '/Users/varunbabbar/PycharmProjects/HackCambridge/HackCambridge/require.js';
var requirejs = require('requirejs');
requirejs.config({
    //Pass the top-level main.js/index.js require
    //function to requirejs so that node modules
    //are loaded relative to the top-level JS file.
    nodeRequire: require
});
const { exec } = require("child_process");
exec("python /Users/varunbabbar/PycharmProjects/HackCambridge/HackCambridge/getLocation.py", (error, stdout, stderr) => {
    if (error) {
        console.log(`error: ${error.message}`);
        return;
    }
    if (stderr) {
        console.log(`stderr: ${stderr}`); 
        return;
    }
    console.log(`stdout: ${stdout}`);
});
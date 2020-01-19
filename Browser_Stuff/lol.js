import { exec } from "child_process";
exec("python ./getLocation.py", (error, stdout, stderr) => {
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



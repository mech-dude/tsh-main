const { spawn } = require('child_process');

// Run a Python script and return output
function runPythonScript(scriptPath) {

  // Use child_process.spawn method from 
  // child_process module and assign it to variable
  const pyProg = spawn('python', [scriptPath]);

  // Collect data from script and print to console
  let data = '';
  pyProg.stdout.on('data', (stdout) => {
    data += stdout.toString();
  });

  // Print errors to console, if any
  pyProg.stderr.on('data', (stderr) => {
    console.log(`stderr: ${stderr}`);
  });

  // When script is finished, print collected data
  pyProg.on('close', (code) => {
    console.log(data);
  });
}

// Run the Python file
runPythonScript('C:/Users/usuario/Desktop/HelpScout API/get_case_nums.py');
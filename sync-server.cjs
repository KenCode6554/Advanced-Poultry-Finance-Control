const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

app.post('/api/sync', (req, res) => {
    console.log('Starting synchronization process...');
    
    // Path to the python script (relative to this file in the dashboard folder)
    const pythonScript = path.join(__dirname, '..', 'tools', 'incremental_sync.py');
    
    // Spawn python process
    const python = spawn('python', [pythonScript]);
    
    let output = '';
    let errorOutput = '';

    python.stdout.on('data', (data) => {
        output += data.toString();
        console.log(`[SYNC]: ${data.toString().trim()}`);
    });

    python.stderr.on('data', (data) => {
        errorOutput += data.toString();
        console.error(`[SYNC ERROR]: ${data.toString().trim()}`);
    });

    python.on('close', (code) => {
        console.log(`Sync process finished with code ${code}`);
        if (code === 0) {
            res.status(200).json({ 
                success: true, 
                message: 'Sync completed successfully',
                output: output
            });
        } else {
            res.status(500).json({ 
                success: false, 
                message: `Sync failed with code ${code}`,
                error: errorOutput
            });
        }
    });
});

app.listen(port, () => {
    console.log(`Sync Bridge Server running at http://localhost:${port}`);
});

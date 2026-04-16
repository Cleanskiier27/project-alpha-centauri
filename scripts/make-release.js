#!/usr/bin/env node
import { execSync } from 'child_process';
import { readFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';

const pkg = JSON.parse(readFileSync('package.json', 'utf8'));
const name = pkg.name || 'networkbuster';
const version = pkg.version || '0.0.0';
const outDir = 'dist';
if (!existsSync(outDir)) mkdirSync(outDir);
const zipName = `${name}-${version}.zip`;

console.log(`Creating ${zipName} in ${outDir}...`);
try {
  if (process.platform === 'win32') {
    // Use PowerShell Compress-Archive
    const files = [
      'server.js', 
      'package.json', 
      'LICENSE', 
      'README.md', 
      'distribution_config.json',
      'launch.py',
      'proxy-server.js',
      'challengerepo/real-time-overlay/dist',
      'database'
    ];
    // Filter out missing files to avoid PowerShell errors
    const existingFiles = files.filter(f => existsSync(f));
    const filesArg = existingFiles.map(f => `"${f}"`).join(',');
    execSync(`powershell -Command "Compress-Archive -Path ${filesArg} -DestinationPath '${join(outDir, zipName)}' -Force"`, { stdio: 'inherit' });
  } else {
    execSync(`zip -r '${join(outDir, zipName)}' server.js package.json LICENSE README.md distribution_config.json launch.py proxy-server.js challengerepo/real-time-overlay/dist database`, { stdio: 'inherit' });
  }
  console.log('Created', join(outDir, zipName));
} catch (e) {
  console.error('Failed to create zip', e);
  process.exit(1);
}
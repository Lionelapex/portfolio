# Launch your portfolio

Paste this single line into a **PowerShell** terminal from any folder:

```powershell
npm.cmd --prefix E:\portfolio install; if ($LASTEXITCODE -eq 0) { npm.cmd --prefix E:\portfolio run dev -- --open }
```

This installs the project's dependencies, starts the React development server, and opens the app in your default browser. Keep the terminal open while using the app. Press **Ctrl+C** to stop it.

Node.js and npm must be installed. They are already available on this machine. Python is not needed to launch the app.

Vite prints the local address in the terminal, usually `http://127.0.0.1:5173/`. If another instance is running, it uses the next available port.

If you move the project, replace `E:\portfolio` in both places with its new folder path. Put paths containing spaces in quotes.

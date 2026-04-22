_FIXES IN app.js_
**Fix 1**
File: app.js
Line: 10
Problem: POST request does not send request body to backend
FROM: axios.post(`${API_URL}/jobs`);
Fix: Changed
TO: axios.post(`${API_URL}/jobs`, req.body);

**Fix 2**
Fix 2
File: app.js
Line: 5
Problem: API URL is hardcoded, making deployment inflexible
FROM: const API_URL = "http://localhost:8000";
Fix: Changed
TO: const API_URL = process.env.API_URL || "http://localhost:8000";

**Fix 3**
File: app.js
Line: 14, 23
Problem: Error handling hides actual error details
FROM: res.status(500).json({ error: "something went wrong" });
Fix: Changed
TO: console.error(err.message);
res.status(500).json({ error: err.message || "Internal Server Error" });

**Fix 4**
File: app.js
Line: 19
Problem: No validation for req.params.id in /status/:id endpoint
Fix: Added validation
TO: const { id } = req.params;

if (!id) {
return res.status(400).json({ error: "ID is required" });
}

**Fix 5**
File: app.js
Line: 6
Problem: No timeout set for external API requests (risk of hanging requests)
Fix: Introduced axios instance with timeout
TO: const axiosInstance = axios.create({ timeout: 5000 });

**Fix 6**
File: app.js
Line: 20, 11
Problem: Using default axios instead of configured instance
FROM: axios.get(...)
axios.post(...)
Fix: Replaced
TO: axiosInstance.get(...)
axiosInstance.post(...)

**Fix 7**
File: app.js
Line: 7
Problem: Static files served from views directory (not standard, may expose unintended files)
FROM: express.static(path.join(**dirname, 'views'))
Fix: Changed
TO: express.static(path.join(**dirname, 'public'))

**Fix 8**
File: app.js
Line: 26
Problem:Port is hardcoded, limiting deployment flexibility
FROM: app.listen(3000, () => {
Fix: Changed
TO: const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {

**Fix 9**
File: app.js
Line: (new addition)
Problem: Missing root endpoint (GET /) required for API validation
Fix: Added
app.get('/', (req, res) => {
res.status(200).json({ message: "API is running" });
});

**Fix 10**
File: app.js
Line: global
Problem: No structured logging for debugging
Fix: Added logging inside catch blocks
console.error(err.message);

_FIXES IN index.html_
**Fix 1**
File: index.html
Line: 22
Problem: No error handling in submitJob() — if request fails, app crashes silently
Fix: Wrapped fetch in try/catch
try {
const res = await fetch('/submit', { method: 'POST' });
const data = await res.json();
} catch (err) {
document.getElementById('result').innerText = "Failed to submit job";
}

**Fix 2**
File: index.html
Line: 23
Problem: No check for HTTP response status before parsing JSON
Fix: Added status validation
if (!res.ok) {
throw new Error("Request failed");
}

**Fix 3**
File: index.html
Line: 24
Problem: Assumes data.job_id always exists
Fix: Added validation
if (!data.job_id) {
throw new Error("Invalid response: missing job_id");
}

**Fix 4**
File: index.html
Line: 28
Problem: jobIds array is unused beyond storing values (wasted memory)
Fix: Remove or use it meaningfully (e.g., tracking jobs in UI)
// Remove if not needed
const jobIds = [];

**Fix 5**
File: index.html
Line: 32
Problem: No error handling in pollJob() — polling can silently fail
Fix: Add try/catch
try {
const res = await fetch(`/status/${id}`);
const data = await res.json();
} catch (err) {
console.error("Polling failed", err);
}

**Fix 6**
File: index.html
Line: 33
Problem: No validation for data.status
Fix: Add fallback
const status = data.status || "unknown";
renderJob(id, status);

**Fix 7**
File: index.html
Line: ~34
Problem: Infinite polling if backend never returns "completed"
Fix: Add retry limit
let retries = 0;
const MAX_RETRIES = 10;

if (data.status !== 'completed' && retries < MAX_RETRIES) {
retries++;
setTimeout(() => pollJob(id), 2000);
}

**Fix 8**
File: index.html
Line: 40
Problem: Using raw id as DOM element ID may cause invalid HTML or conflicts
Fix: Sanitize ID
el.id = `job-${id}`;

**Fix 9**
File: index.html
Line: 44
Problem: id.substring(0, 8) assumes id is a string
Fix: Ensure type safety
const shortId = String(id).substring(0, 8);

**FIx 10**
File: index.html
Line: global
Problem: No loading state for user feedback
Fix: Add UI feedback
document.getElementById('result').innerText = "Submitting job...";

**Fix 11**
File: index.html
Line: global
Problem: No Content-Type header in POST request
Fix: Add headers (future-proof if sending data)
fetch('/submit', {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({})
});

**Fix 12**
File: index.html
Line: global
Problem: No debounce or button disable → user can spam requests
Fix: Disable button during request
const btn = document.querySelector('button');
btn.disabled = true;
// after request
btn.disabled = false;

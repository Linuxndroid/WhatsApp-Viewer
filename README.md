<p align="center">
<img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhOe-tzXfWFtQ6pew7MCq8rPtn6aY-HfBfGBTcnupqllQJ6kf1aWqszKyqgZ9yHntK-wBkAw1AedZFzzLUipNmMEBBixkhpeeTeJVBpBld7LW2YA4ZjnzSUuCx9Ou_16jVmjLZRTCJer-nUTIZcwqRNc7TEZZCX35vGJ8_zpH01QhYI6okNQcL7B-7idQ/s320/20230509_103108.png" height="100"><br>
</p>
<h1 align="center">Linuxndroid WhatsApp-View</h1>
<p align="center">
A Python GUI application for extracting WhatsApp chat conversations from the app's SQLite database and viewing them in a simple, user-friendly desktop app.
</p>

<p align="center">
  <img src="https://github.com/Linuxndroid/WhatsApp-Viewer/blob/main/resources/1.png" alt="Screenshot of App" width="700">
</p>

<h2>Features</h2>
<ul>
<li><strong>Easy-to-Use GUI:</strong> No more command lines or running a web server. Just run the app and load your files.</li>
<li><strong>Light &amp; Dark Modes:</strong> Includes a theme toggle for your comfort.</li>
<li><strong>Chat-Style Viewing:</strong> Reads all messages and displays them in a familiar sent/received chat bubble format.</li>
<li><strong>Contact Name Support:</strong> Automatically loads contact names from your <code>wa.db</code> file.</li>
<li><strong>Standalone:</strong> Can be compiled into a single <code>.exe</code> file for Windows, with no Python installation required.</li>
</ul>
<hr>
<h2>How to Use (Recommended for Users)</h2>
<p>You can download the pre-compiled application from the <strong>Releases</strong> page.</p>
<ol>
<li>Go to the <a href="https://github.com/Linuxndroid/WhatsApp-Viewer/releases/download/v.1.0/Linuxndroid-WhatsApp-View.exe"><strong>Releases</strong></a> page of this repository. </li>
<li>Download the latest <code>Linuxndroid-WhatsApp-View.exe</code> file.</li>
<li>Run the <code>.exe</code> file. (No installation is needed).</li>
<li>You will first need your <strong>decrypted database files</strong>. You can get them using <a href="https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor">WhatsApp-Key-Database-Extractor</a>.</li>
<li>In the app, click the first "Browse" button to select your <code>msgstore.db</code> file.</li>
<li>Click the second "Browse" button to select your <code>wa.db</code> file (this is optional but provides contact names).</li>
<li>Click "Load Chats" and start reading!</li>
</ol>
<hr>
<h2>How to Run from Source (For Developers)</h2>
<p>If you prefer to run the script directly using Python:</p>
<ol>
<li><strong>Get Database Files:</strong> You must have your decrypted WhatsApp database files. Use <a href="https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor">Whatsapp Key Extractor</a> for this.</li>
<li><strong>Clone the Repository:</strong>
<pre><code>git clone https://github.com/your-username/WhatsApp-Viewer.git
cd WhatsApp-Viewer
</code></pre>
</li>
<li><strong>Install Dependencies:</strong>
This project only relies on Python's built-in libraries (like Tkinter). No <code>pip install</code> is required.</li>
<li><strong>Run the GUI:</strong>
Instead of <code>main.py</code>, you will now run <code>gui.py</code>:
<pre><code>python3 gui.py
</code></pre>
</li>
<li>Use the application as described in the section above.</li>
</ol>
<hr>
<h2>How to Build the <code>.exe</code> (For Developers)</h2>
<p>If you want to compile the executable yourself:</p>
<ol>
<li><strong>Install PyInstaller:</strong>
<pre><code>pip install pyinstaller
</code></pre>
</li>
<li><strong>Add Your Icon:</strong>
Place your desired icon file named <code>icon.ico</code> in the root of the project directory.</li>
<li><strong>Run the Build Command:</strong>
From the project's root directory, run the following command:
<pre><code>pyinstaller --onefile --windowed --name "Linuxndroid-WhatsApp-View" --icon="icon.ico" gui.py
</code></pre>
</li>
<li><strong>Find Your App:</strong>
Your standalone <code>Linuxndroid-WhatsApp-View.exe</code> file will be in the newly created <code>dist/</code> folder.</li>
</ol>
<hr>
<h2>Disclaimer</h2>
<p><b>Linuxndroid Provides no warranty with this software and will not be responsible for any direct or indirect damage caused due to the usage of this tool.<br>
This tool is built for both Educational and Internal use ONLY.</b></p>
<br>
<p align="center">Made with ❤️ By <a href="https://www.youtube.com/channel/UC2O1Hfg-dDCbUcau5QWGcgg">Linuxndroid</a></p>
<h2>Credit</h2>
<p>This project is an enhancement of the original CLI script by <a href="https://github.com/chrrel">chrrel</a>.</p>
<h2>Follow Me on :</h2>
<p><a href="https://www.instagram.com/linuxndroid"><img src="https://img.shields.io/badge/IG-linuxndroid-yellowgreen?style=for-the-badge&logo=instagram" alt="Instagram"></a>
<a href="https://www.youtube.com/channel/UC2O1Hfg-dDCbUcau5QWGcgg"><img src="https://img.shields.io/badge/Youtube-linuxndroid-redgreen?style=for-the-badge&logo=youtube" alt="Youtube"></a>
<a href="https://www.linuxndroid.com"><img src="https://img.shields.io/badge/Website-linuxndroid-yellowred?style=for-the-badge&logo=browser" alt="Browser"></a></p>

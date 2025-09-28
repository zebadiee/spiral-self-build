
#!/usr/bin/env python3
"""
Tkinter Simple Dashboard
Streamlined dashboard with real-time metrics for the self-learning assistant.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import threading
import time
from datetime import datetime
from typing import Dict, Any

class SLSADashboard:
    """Simple dashboard for monitoring SLSA metrics."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SLSA Dashboard - Self-Learning Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.server_url = "http://localhost:8001"
        self.update_interval = 5  # seconds
        self.running = True
        
        self.setup_ui()
        self.start_monitoring()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🧠 SLSA Dashboard",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Main content area
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Status section
        self.setup_status_section(main_frame)
        
        # Metrics section
        self.setup_metrics_section(main_frame)
        
        # Recent insights section
        self.setup_insights_section(main_frame)
        
        # Control buttons
        self.setup_controls(main_frame)
    
    def setup_status_section(self, parent):
        """Set up server status section."""
        status_frame = tk.LabelFrame(parent, text="Server Status", font=('Arial', 12, 'bold'))
        status_frame.pack(fill='x', pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="🔴 Checking...",
            font=('Arial', 11),
            fg='red'
        )
        self.status_label.pack(pady=10)
        
        self.last_update_label = tk.Label(
            status_frame,
            text="Last update: Never",
            font=('Arial', 9),
            fg='gray'
        )
        self.last_update_label.pack()
    
    def setup_metrics_section(self, parent):
        """Set up metrics display section."""
        metrics_frame = tk.LabelFrame(parent, text="Learning Metrics", font=('Arial', 12, 'bold'))
        metrics_frame.pack(fill='x', pady=5)
        
        # Create metrics grid
        metrics_grid = tk.Frame(metrics_frame)
        metrics_grid.pack(fill='x', padx=10, pady=10)
        
        # Sessions metric
        sessions_frame = tk.Frame(metrics_grid, bg='#3498db', relief='raised', bd=2)
        sessions_frame.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        
        tk.Label(sessions_frame, text="Learning Sessions", bg='#3498db', fg='white', font=('Arial', 10, 'bold')).pack()
        self.sessions_count = tk.Label(sessions_frame, text="0", bg='#3498db', fg='white', font=('Arial', 16, 'bold'))
        self.sessions_count.pack()
        
        # Insights metric
        insights_frame = tk.Frame(metrics_grid, bg='#2ecc71', relief='raised', bd=2)
        insights_frame.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(insights_frame, text="Total Insights", bg='#2ecc71', fg='white', font=('Arial', 10, 'bold')).pack()
        self.insights_count = tk.Label(insights_frame, text="0", bg='#2ecc71', fg='white', font=('Arial', 16, 'bold'))
        self.insights_count.pack()
        
        # Configure grid weights
        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
    
    def setup_insights_section(self, parent):
        """Set up recent insights display."""
        insights_frame = tk.LabelFrame(parent, text="Recent Insights", font=('Arial', 12, 'bold'))
        insights_frame.pack(fill='both', expand=True, pady=5)
        
        # Create scrollable text area
        text_frame = tk.Frame(insights_frame)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.insights_text = tk.Text(
            text_frame,
            wrap='word',
            font=('Arial', 10),
            bg='white',
            fg='black',
            state='disabled'
        )
        
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.insights_text.yview)
        self.insights_text.configure(yscrollcommand=scrollbar.set)
        
        self.insights_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def setup_controls(self, parent):
        """Set up control buttons."""
        controls_frame = tk.Frame(parent, bg='#f0f0f0')
        controls_frame.pack(fill='x', pady=10)
        
        # Refresh button
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh Now",
            command=self.manual_refresh,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        )
        refresh_btn.pack(side='left', padx=5)
        
        # Test learning button
        test_btn = tk.Button(
            controls_frame,
            text="🧪 Test Learning",
            command=self.test_learning,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='raised',
            bd=2
        )
        test_btn.pack(side='left', padx=5)
        
        # Server URL entry
        tk.Label(controls_frame, text="Server:", bg='#f0f0f0').pack(side='right', padx=5)
        self.server_entry = tk.Entry(controls_frame, width=25)
        self.server_entry.insert(0, self.server_url)
        self.server_entry.pack(side='right', padx=5)
    
    def start_monitoring(self):
        """Start the monitoring thread."""
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                self.update_dashboard()
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(self.update_interval)
    
    def update_dashboard(self):
        """Update dashboard with latest data."""
        try:
            # Update server URL from entry
            self.server_url = self.server_entry.get()
            
            # Get server status
            status_response = requests.get(f"{self.server_url}/status", timeout=5)
            if status_response.status_code == 200:
                status_data = status_response.json()
                self.update_status(True, status_data)
            else:
                self.update_status(False, {"error": f"HTTP {status_response.status_code}"})
            
            # Get metrics
            metrics_response = requests.get(f"{self.server_url}/metrics", timeout=5)
            if metrics_response.status_code == 200:
                metrics_data = metrics_response.json()
                self.update_metrics(metrics_data)
            
            # Get recent insights
            insights_response = requests.get(f"{self.server_url}/insights?limit=5", timeout=5)
            if insights_response.status_code == 200:
                insights_data = insights_response.json()
                self.update_insights(insights_data)
                
        except requests.exceptions.ConnectionError:
            self.update_status(False, {"error": "Connection failed"})
        except Exception as e:
            self.update_status(False, {"error": str(e)})
    
    def update_status(self, is_healthy: bool, data: Dict[str, Any]):
        """Update server status display."""
        if is_healthy:
            status_text = "🟢 Server Online"
            status_color = "green"
        else:
            status_text = f"🔴 Server Offline - {data.get('error', 'Unknown error')}"
            status_color = "red"
        
        self.status_label.config(text=status_text, fg=status_color)
        self.last_update_label.config(text=f"Last update: {datetime.now().strftime('%H:%M:%S')}")
    
    def update_metrics(self, data: Dict[str, Any]):
        """Update metrics display."""
        session_count = data.get('session_count', 0)
        insight_count = data.get('insight_count', 0)
        
        self.sessions_count.config(text=str(session_count))
        self.insights_count.config(text=str(insight_count))
    
    def update_insights(self, data: Dict[str, Any]):
        """Update insights display."""
        insights = data.get('insights', [])
        
        self.insights_text.config(state='normal')
        self.insights_text.delete(1.0, tk.END)
        
        if insights:
            for i, insight in enumerate(insights[-5:], 1):  # Show last 5
                self.insights_text.insert(tk.END, f"{i}. {insight}\n\n")
        else:
            self.insights_text.insert(tk.END, "No insights available yet.\nTry processing a document with the knowledge ingestion system.")
        
        self.insights_text.config(state='disabled')
    
    def manual_refresh(self):
        """Manually refresh the dashboard."""
        self.update_dashboard()
    
    def test_learning(self):
        """Test the learning system with sample content."""
        try:
            test_content = "This is a test document for the self-learning assistant system. It contains sample data to verify that the learning pipeline is working correctly."
            
            response = requests.post(
                f"{self.server_url}/learn",
                json={
                    "content": test_content,
                    "source": "dashboard_test",
                    "metadata": {"test": True}
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                messagebox.showinfo(
                    "Test Successful",
                    f"Learning test completed!\nGenerated {len(result['insights'])} insights."
                )
                self.update_dashboard()  # Refresh to show new data
            else:
                messagebox.showerror("Test Failed", f"Server error: {response.status_code}")
                
        except Exception as e:
            messagebox.showerror("Test Failed", f"Error: {str(e)}")
    
    def run(self):
        """Start the dashboard."""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
    
    def on_closing(self):
        """Handle application closing."""
        self.running = False
        self.root.quit()
        self.root.destroy()

def main():
    """Main function."""
    print("🚀 Starting SLSA Dashboard...")
    print("📊 Dashboard will open in a new window")
    print("🔗 Make sure MCP server is running on http://localhost:8001")
    
    dashboard = SLSADashboard()
    dashboard.run()

if __name__ == "__main__":
    main()

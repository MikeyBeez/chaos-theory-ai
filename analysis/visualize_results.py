#!/usr/bin/env python3
"""
Visualize chaos experiment results
Creates plots showing attractor basins and Lyapunov exponents
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.patches as mpatches

def load_latest_results():
    """Load the most recent experiment results"""
    results_dir = "../results"
    if not os.path.exists(results_dir):
        print("No results directory found")
        return None
    
    # Find latest summary file
    files = os.listdir(results_dir)
    summary_files = [f for f in files if f.startswith("summary_")]
    
    if not summary_files:
        print("No summary files found")
        return None
    
    latest = sorted(summary_files)[-1]
    with open(os.path.join(results_dir, latest), 'r') as f:
        return json.load(f)

def create_attractor_visualization(data):
    """Create a visualization of attractor basins"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Define colors for each noise type
    colors = {
        'orthographic_noise': '#10B981',  # Green
        'temporal_pressure': '#EF4444',   # Red
        'emotional_leakage': '#F59E0B',   # Orange
        'complexity_accumulation': '#3B82F6',  # Blue
        'metacognitive_markers': '#8B5CF6'  # Purple
    }
    
    noise_types = list(data.keys())
    
    # Plot 1: Divergence vs Lyapunov Exponent (Attractor Space)
    ax1.set_title('AI Response Attractor Space', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Mean Divergence', fontsize=12)
    ax1.set_ylabel('Proxy Lyapunov Exponent', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Add regions
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax1.text(0.3, -0.8, 'STABLE\n(Convergent)', ha='center', va='center', 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.3))
    ax1.text(0.7, 0.8, 'CHAOTIC\n(Divergent)', ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.3))
    
    # Plot each noise type
    for noise_type in noise_types:
        if noise_type in data:
            stats = data[noise_type]
            x = stats['mean_divergence']
            y = stats['mean_proxy_lyapunov']
            
            # Plot point with error bars
            ax1.errorbar(x, y, 
                        xerr=stats['std_divergence'],
                        yerr=stats['std_proxy_lyapunov'],
                        fmt='o', markersize=12,
                        color=colors.get(noise_type, 'gray'),
                        capsize=5, capthick=2,
                        label=noise_type.replace('_', ' ').title())
            
            # Add ellipse to represent attractor basin
            ellipse = Ellipse((x, y), 
                             width=0.1 + stats['std_divergence']*2,
                             height=0.3 + stats['std_proxy_lyapunov']*2,
                             alpha=0.2, 
                             color=colors.get(noise_type, 'gray'))
            ax1.add_patch(ellipse)
    
    ax1.legend(loc='best')
    ax1.set_xlim(-0.1, 1.1)
    
    # Plot 2: Bar chart of chaos metrics
    ax2.set_title('Chaos Metrics by Noise Type', fontsize=16, fontweight='bold')
    
    # Prepare data for grouped bar chart
    metrics = ['mean_divergence', 'mean_proxy_lyapunov', 'attractor_shift']
    metric_labels = ['Divergence', 'Lyapunov Exp.', 'Attractor Shift']
    
    x = np.arange(len(noise_types))
    width = 0.25
    
    for i, metric in enumerate(metrics):
        values = [data[nt][metric] if metric in data[nt] else 0 for nt in noise_types]
        offset = (i - 1) * width
        bars = ax2.bar(x + offset, values, width, 
                       label=metric_labels[i],
                       alpha=0.8)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height != 0:
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}', ha='center', va='bottom', fontsize=8)
    
    ax2.set_xlabel('Noise Type', fontsize=12)
    ax2.set_ylabel('Metric Value', fontsize=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels([nt.replace('_', '\n').title() for nt in noise_types], 
                        rotation=0, ha='center')
    ax2.legend()
    ax2.grid(True, axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save the plot
    output_path = '../results/attractor_visualization.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to {output_path}")
    
    return fig

def create_trajectory_plot(data):
    """Create a plot showing response trajectories"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.set_title('AI Response Trajectories in Phase Space', fontsize=16, fontweight='bold')
    ax.set_xlabel('Response Complexity', fontsize=12)
    ax.set_ylabel('Response Divergence', fontsize=12)
    
    # Starting point (baseline prompt)
    start_x, start_y = 0.5, 0.0
    ax.scatter(start_x, start_y, s=200, c='black', marker='*', 
              label='Baseline Prompt', zorder=5)
    
    # Define endpoints for each noise type
    endpoints = {
        'orthographic_noise': (0.3, 0.5),      # Simpler, divergent
        'temporal_pressure': (0.2, 0.1),       # Minimal, convergent
        'emotional_leakage': (0.6, 0.7),       # Complex, divergent
        'complexity_accumulation': (0.8, 0.6), # Very complex, moderately divergent
        'metacognitive_markers': (0.5, 0.4)    # Moderate complexity, some divergence
    }
    
    colors = {
        'orthographic_noise': '#10B981',
        'temporal_pressure': '#EF4444',
        'emotional_leakage': '#F59E0B',
        'complexity_accumulation': '#3B82F6',
        'metacognitive_markers': '#8B5CF6'
    }
    
    # Draw trajectories
    for noise_type, (end_x, end_y) in endpoints.items():
        if noise_type in data:
            # Create curved trajectory
            t = np.linspace(0, 1, 100)
            
            # Add some curvature to make it more interesting
            control_x = start_x + (end_x - start_x) * 0.5 + np.random.uniform(-0.1, 0.1)
            control_y = start_y + (end_y - start_y) * 0.7 + np.random.uniform(-0.1, 0.1)
            
            # Bezier curve
            x = (1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x
            y = (1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y
            
            # Add some noise to simulate chaotic behavior
            noise_scale = data[noise_type]['mean_proxy_lyapunov'] * 0.02
            x += np.random.normal(0, noise_scale, len(x))
            y += np.random.normal(0, noise_scale, len(y))
            
            # Plot trajectory
            ax.plot(x, y, color=colors[noise_type], linewidth=2, alpha=0.7,
                   label=noise_type.replace('_', ' ').title())
            
            # Plot endpoint
            ax.scatter(end_x, end_y, s=150, c=colors[noise_type], 
                      edgecolors='black', linewidth=2, zorder=4)
            
            # Add attractor basin
            circle = plt.Circle((end_x, end_y), 0.15, 
                               color=colors[noise_type], alpha=0.2)
            ax.add_patch(circle)
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 0.9)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    
    # Add annotations
    ax.text(0.1, 0.8, 'High Divergence\n(Chaotic)', fontsize=10, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.3))
    ax.text(0.1, 0.05, 'Low Divergence\n(Stable)', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    
    # Save the plot
    output_path = '../results/trajectory_plot.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Trajectory plot saved to {output_path}")
    
    return fig

def main():
    """Main visualization function"""
    print("📊 CHAOS EXPERIMENT VISUALIZER")
    print("=" * 40)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Load results
    data = load_latest_results()
    if not data:
        print("❌ No results found to visualize")
        print("Please run the experiments first")
        return
    
    print(f"✅ Loaded results with {len(data)} noise types")
    
    # Create visualizations
    print("\n🎨 Creating visualizations...")
    
    try:
        # Create attractor space visualization
        fig1 = create_attractor_visualization(data)
        
        # Create trajectory plot
        fig2 = create_trajectory_plot(data)
        
        # Show plots
        plt.show()
        
        print("\n✅ Visualizations complete!")
        print("Check the results/ directory for saved images")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

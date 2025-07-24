#!/usr/bin/env python3
"""
Comprehensive Game Analysis Suite
Single script to run all simulations and generate academic visualizations
"""

import os
import sys
import json
import time
from datetime import datetime

# Add games directory to path
sys.path.append('games')

def run_comprehensive_analysis():
    """Run complete analysis suite"""
    print("=" * 60)
    print("COMPREHENSIVE GAME ANALYSIS SUITE")
    print("=" * 60)
    
    # Step 1: Run comprehensive simulations
    print("\n1. Running comprehensive simulations...")
    os.system('python run_comprehensive_simulations.py')
    
    # Step 2: Generate academic visualizations
    print("\n2. Generating academic visualizations...")
    os.system('python generate_academic_visualizations.py')
    
    # Step 3: Verify outputs
    print("\n3. Verifying outputs...")
    
    # Check for simulation data
    data_files = [f for f in os.listdir('output') if f.startswith('comprehensive_simulation_results_') and f.endswith('.json')]
    if data_files:
        latest_data = sorted(data_files)[-1]
        print(f"   ✓ Latest simulation data: {latest_data}")
    else:
        print("   ✗ No simulation data found")
    
    # Check for visualizations
    required_images = [
        'game_win_rates_comparison.png',
        'performance_analysis.png', 
        'algorithm_effectiveness.png',
        'search_depth_analysis.png',
        'comprehensive_summary.png',
        'halving_win_rates.png',
        'tic_tac_toe_win_rates.png'
    ]
    
    missing_images = []
    for img in required_images:
        if os.path.exists(f'output/images/{img}'):
            print(f"   ✓ {img}")
        else:
            missing_images.append(img)
            print(f"   ✗ {img}")
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    if not missing_images:
        print("✓ All required files generated successfully")
        print("\nGenerated files:")
        print("  - Simulation data: output/comprehensive_simulation_results_*.json")
        print("  - Academic visualizations: output/images/*.png")
        print("  - LaTeX report: report_extended.tex")
        print("\nTo compile the report: ./compile_extended_report.sh")
    else:
        print(f"✗ Missing {len(missing_images)} required images")
        for img in missing_images:
            print(f"    - {img}")

if __name__ == "__main__":
    run_comprehensive_analysis()
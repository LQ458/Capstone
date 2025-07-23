import matplotlib.pyplot as plt
import numpy as np

# Set font and style
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_tic_tac_toe_win_rate_chart():
    """Create Tic-Tac-Toe win rate comparison chart"""
    # Simulation data
    scenarios = ['Minimax vs Random', 'Minimax vs Minimax', 'Random vs Random']
    win_rates = [98, 50, 33]  # Example data
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(scenarios, win_rates, color=['#2E8B57', '#4682B4', '#CD5C5C'], alpha=0.8)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Game Scenario', fontsize=12)
    plt.ylabel('Win Rate (%)', fontsize=12)
    plt.title('Tic-Tac-Toe Agent Performance Analysis', fontsize=16, fontweight='bold')
    plt.ylim(0, 100)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/images/tic_tac_toe_win_rates.png', dpi=300, bbox_inches='tight')
    print("Tic-Tac-Toe win rates chart saved to output/images/tic_tac_toe_win_rates.png")

if __name__ == "__main__":
    create_tic_tac_toe_win_rate_chart() 
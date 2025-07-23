import matplotlib.pyplot as plt
import numpy as np

# Set font and style
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_halving_win_rate_chart():
    """Create Halving game win rate chart"""
    # Simulation data
    initial_numbers = [10, 20, 30, 50, 100]
    player1_win_rates = [60, 55, 52, 48, 45]  # Example data
    player2_win_rates = [40, 45, 48, 52, 55]
    
    x = np.arange(len(initial_numbers))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    bars1 = plt.bar(x - width/2, player1_win_rates, width, label='Player 1 (First)', color='#2E8B57', alpha=0.8)
    bars2 = plt.bar(x + width/2, player2_win_rates, width, label='Player 2 (Second)', color='#4682B4', alpha=0.8)
    
    plt.xlabel('Initial Number', fontsize=12)
    plt.ylabel('Win Rate (%)', fontsize=12)
    plt.title('Halving Game Win Rate Distribution by Initial Number', fontsize=16, fontweight='bold')
    plt.xticks(x, initial_numbers)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('../../output/images/halving_win_rates.png', dpi=300, bbox_inches='tight')
    print("Halving win rates chart saved to output/images/halving_win_rates.png")

if __name__ == "__main__":
    create_halving_win_rate_chart() 
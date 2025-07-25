import matplotlib.pyplot as plt
import os

os.makedirs('output/images', exist_ok=True)
import random
from game import ConnectFour
import test as c4f

games = 100

def simulate_game(agent1, agent2):
    results = {'X': 0, 'O': 0}
    for _ in range(games):
        game = ConnectFour()
        while True:
            if game.current_player == 'X':
                if agent1 == 'random':
                    move = random.choice(game.get_valid_moves())
                else:
                    move = game.best_move(agent1)
            else:
                if agent2 == 'random':
                    move = random.choice(game.get_valid_moves())
                else:
                    move = game.best_move(agent2)
            game.make_move(move)
            if c4f.win(game.bitboard['X']):
                results['X'] += 1
                break
            if c4f.win(game.bitboard['O']):
                results['O'] += 1
                break
            if not game.get_valid_moves():
                break
    return results

def create_random_vs_6_chart():
    res = simulate_game('random', 8)
    rates = [res['X']/games*100, res['O']/games*100]
    labels = ['X: random', 'O: minimax d=6']

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, rates, color=['#4C72B0', '#55A868'], alpha=0.8)
    ax.set_title('Random vs Minimax d=6', fontsize=14)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_ylim(0, 100)
    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x()+bar.get_width()/2, rate+1, f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=11)
    plt.tight_layout()
    plt.savefig('output/images/c4_random_vs_8.png', dpi=300)
    plt.show()

def create_depth8_vs_6_chart():
    res = simulate_game(8, 6)
    rates = [res['X']/games*100, res['O']/games*100]
    labels = ['X: d=8', 'O: d=6']

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, rates, color=['#4C72B0', '#55A868'], alpha=0.8)
    ax.set_title('Minimax d=8 vs d=6', fontsize=14)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_ylim(0, 100)
    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x()+bar.get_width()/2, rate+1, f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=11)
    plt.tight_layout()
    plt.savefig('output/images/c4_d8_vs_d6.png', dpi=300)
    plt.show()

def create_depth8_vs_8_chart():
    res = simulate_game(6, 6)
    rates = [res['X']/games*100, res['O']/games*100]
    labels = ['X: d=6', 'O: d=6']

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, rates, color=['#4C72B0', '#55A868'], alpha=0.8)
    ax.set_title('Minimax d=6 vs d=6', fontsize=14)
    ax.set_ylabel('Win Rate (%)', fontsize=12)
    ax.set_ylim(0, 100)
    for bar, rate in zip(bars, rates):
        ax.text(bar.get_x()+bar.get_width()/2, rate+1, f'{rate:.1f}%',
                ha='center', va='bottom', fontsize=11)
    plt.tight_layout()
    plt.savefig('output/images/c4_d8_vs_d8.png', dpi=300)
    plt.show()

if __name__ == '__main__':
    create_random_vs_6_chart()
    create_depth8_vs_6_chart()
    create_depth8_vs_8_chart()

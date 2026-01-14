// ============== USER PANEL ==============
function updateUserPanel() {
    const panel = document.getElementById('userPanel');
    if (!panel) return;
    
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');
    const coins = localStorage.getItem('coins');
    
    if (userId && username) {
        panel.innerHTML = `
            <span class="username">🎰 ${username}</span>
            <span class="coins">${coins} 💰</span>
            <a href="/user/${userId}" class="btn btn-sm" style="background: var(--bg-secondary); color: var(--text-primary); padding: 0.5rem 1rem;">Profile</a>
        `;
        panel.style.display = 'flex';
        
        // Hide register box if exists
        const registerBox = document.getElementById('registerBox');
        if (registerBox && !registerBox.classList.contains('hidden')) {
            registerBox.innerHTML = `
                <div class="welcome-back">
                    <h3>🎰 Welcome back, ${username}!</h3>
                    <p>You have <span class="coins">${coins}</span> coins</p>
                    <p>Browse departments below to place your bets!</p>
                </div>
            `;
        }
    } else {
        panel.innerHTML = '';
        panel.style.display = 'none';
    }
}

// ============== REFRESH USER DATA ==============
async function refreshUserData() {
    const userId = localStorage.getItem('user_id');
    if (!userId) return;
    
    try {
        const response = await fetch(`/api/user/${userId}`);
        const data = await response.json();
        localStorage.setItem('coins', data.coins);
        updateUserPanel();
    } catch (error) {
        console.error('Failed to refresh user data:', error);
    }
}

// ============== INITIALIZE ==============
document.addEventListener('DOMContentLoaded', () => {
    updateUserPanel();
    
    // Refresh user data every 30 seconds
    setInterval(refreshUserData, 30000);
    
    // Add some fun console messages
    console.log('%c💀 LAYOFF MARKET 💀', 'font-size: 24px; font-weight: bold; color: #ff3b3b;');
    console.log('%cWhere careers come to die...', 'font-style: italic; color: #9898a8;');
    console.log('%c⚠️ This is satire. Please don\'t fire anyone based on betting odds.', 'color: #ff9500;');
});

// ============== EASTER EGG ==============
let konamiCode = [];
const konamiSequence = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.keyCode);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        document.body.style.animation = 'shake 0.5s ease-in-out';
        alert('🎉 KONAMI CODE ACTIVATED!\n\nJust kidding, everyone is still getting laid off. 💀');
        setTimeout(() => {
            document.body.style.animation = '';
        }, 500);
    }
});

// Add shake animation
const style = document.createElement('style');
style.textContent = `
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}
`;
document.head.appendChild(style);


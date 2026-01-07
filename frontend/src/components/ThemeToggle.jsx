import './ThemeToggle.css'

function ThemeToggle({ theme, onToggle }) {
    return (
        <button
            className="theme-toggle"
            onClick={onToggle}
            aria-label="Toggle theme"
        >
            {theme === 'dark' ? '☀️' : '🌙'}
        </button>
    )
}

export default ThemeToggle

import { useEffect, useRef } from 'react'
import './WelcomePage.css'

function WelcomePage({ onGetStarted }) {
    const containerRef = useRef(null)
    const canvasRef = useRef(null)

    useEffect(() => {
        const container = containerRef.current
        const canvas = canvasRef.current
        if (!canvas) return

        const ctx = canvas.getContext('2d')
        canvas.width = window.innerWidth
        canvas.height = window.innerHeight

        // Particle system
        const particles = []
        const particleCount = 80

        class Particle {
            constructor() {
                this.reset()
                this.y = Math.random() * canvas.height
            }

            reset() {
                this.x = Math.random() * canvas.width
                this.y = -10
                this.speed = Math.random() * 2 + 1
                this.size = Math.random() * 3 + 1
                this.opacity = Math.random() * 0.5 + 0.3
                this.color = ['#60a5fa', '#a78bfa', '#ec4899'][Math.floor(Math.random() * 3)]
            }

            update() {
                this.y += this.speed
                if (this.y > canvas.height) {
                    this.reset()
                }
            }

            draw() {
                ctx.beginPath()
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
                ctx.fillStyle = this.color
                ctx.globalAlpha = this.opacity
                ctx.fill()
                ctx.globalAlpha = 1
            }
        }

        // Initialize particles
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle())
        }

        // Mouse tracking
        let mouseX = 0
        let mouseY = 0
        const handleMouseMove = (e) => {
            mouseX = e.clientX
            mouseY = e.clientY

            // Create ripple effect
            const ripple = document.createElement('div')
            ripple.className = 'mouse-ripple'
            ripple.style.left = mouseX + 'px'
            ripple.style.top = mouseY + 'px'
            container.appendChild(ripple)

            setTimeout(() => ripple.remove(), 1000)
        }

        container.addEventListener('mousemove', handleMouseMove)

        // Animation loop
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            // Draw connections between nearby particles
            particles.forEach((p1, i) => {
                particles.slice(i + 1).forEach(p2 => {
                    const dx = p1.x - p2.x
                    const dy = p1.y - p2.y
                    const distance = Math.sqrt(dx * dx + dy * dy)

                    if (distance < 150) {
                        ctx.beginPath()
                        ctx.moveTo(p1.x, p1.y)
                        ctx.lineTo(p2.x, p2.y)
                        ctx.strokeStyle = '#60a5fa'
                        ctx.globalAlpha = (1 - distance / 150) * 0.2
                        ctx.stroke()
                        ctx.globalAlpha = 1
                    }
                })

                p1.update()
                p1.draw()
            })

            requestAnimationFrame(animate)
        }

        animate()

        // Resize handler
        const handleResize = () => {
            canvas.width = window.innerWidth
            canvas.height = window.innerHeight
        }

        window.addEventListener('resize', handleResize)

        return () => {
            container.removeEventListener('mousemove', handleMouseMove)
            window.removeEventListener('resize', handleResize)
        }
    }, [])

    return (
        <div className="welcome-container" ref={containerRef}>
            <canvas ref={canvasRef} className="particle-canvas"></canvas>
            
            <div className="welcome-content glass fade-in">
                <div className="logo-section">
                    <div className="logo-icon"></div>
                </div>

                <div className="title-section">
                    <h1 className="product-name">RideMatch AI</h1>
                    <p className="tagline">AI-Powered Ride Matching & Dynamic Pricing</p>
                </div>

                <div className="description-section">
                    <p>
                        Smart vehicle recommendations powered by machine learning.
                        Get accurate ETAs, fair prices, and the best ride for your needs.
                    </p>
                </div>

                <button className="cta-button" onClick={onGetStarted}>
                    <span>Plan Your Ride</span>
                    <span className="arrow"></span>
                </button>

                <div className="features-grid">
                    <div className="feature-card">
                        <div className="feature-icon"></div>
                        <h3>AI ETA Prediction</h3>
                        <p>Real-time arrival estimates</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon"></div>
                        <h3>Dynamic Pricing</h3>
                        <p>Fair, demand-based fares</p>
                    </div>
                    <div className="feature-card">
                        <div className="feature-icon"></div>
                        <h3>Smart Ranking</h3>
                        <p>Best vehicle for your trip</p>
                    </div>
                </div>

                <div className="demo-badge">
                    <small> Demo Mode  Powered by ML Models</small>
                </div>
            </div>

            <div className="floating-elements">
                <div className="float-item float-1"></div>
                <div className="float-item float-2"></div>
                <div className="float-item float-3"></div>
                <div className="float-item float-4"></div>
            </div>
        </div>
    )
}

export default WelcomePage

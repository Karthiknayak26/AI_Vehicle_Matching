import { useState, useEffect } from 'react'
import './AIProcessingOverlay.css'

const PROCESSING_STEPS = [
    { text: "Analyzing traffic patterns...", icon: "🚦", duration: 1000 },
    { text: "Predicting ETA with ML model...", icon: "🤖", duration: 1000 },
    { text: "Calculating optimal pricing...", icon: "💰", duration: 1000 }
]

function AIProcessingOverlay() {
    const [currentStep, setCurrentStep] = useState(0)
    const [completedSteps, setCompletedSteps] = useState([])

    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentStep(prev => {
                if (prev < PROCESSING_STEPS.length) {
                    setCompletedSteps(completed => [...completed, prev])
                    return prev + 1
                }
                return prev
            })
        }, 1000)

        return () => clearInterval(timer)
    }, [])

    const progress = ((currentStep) / PROCESSING_STEPS.length) * 100

    return (
        <div className="ai-overlay">
            <div className="ai-card glass fade-in">
                <div className="ai-header">
                    <div className="ai-icon spin">⚡</div>
                    <h2>AI Processing...</h2>
                </div>

                <div className="ai-steps">
                    {PROCESSING_STEPS.map((step, index) => (
                        <div
                            key={index}
                            className={`ai-step ${completedSteps.includes(index) ? 'completed' : ''} ${currentStep === index ? 'active' : ''}`}
                        >
                            <div className="step-icon">
                                {completedSteps.includes(index) ? '✓' : step.icon}
                            </div>
                            <div className="step-text">{step.text}</div>
                        </div>
                    ))}
                </div>

                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${progress}%` }}
                    />
                </div>

                <div className="ai-footer">
                    <small>Powered by LightGBM ML Model</small>
                </div>
            </div>
        </div>
    )
}

export default AIProcessingOverlay

/**
 * AETHER-UI v1.0.0
 * The Aesthetic Engine for High-Fidelity Neural OS interfaces.
 */

export const AetherStyles = {
    glass: "backdrop-filter: blur(25px) saturate(150%); background: rgba(15, 15, 25, 0.85); border: 1px solid rgba(255,255,255,0.1);",
    accent: "#00d2ff",
    purple: "#9d50bb",
    success: "#00ff9d"
};

export class AetherVisuals {
    static initParticles(canvasId) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let w = canvas.width = canvas.offsetWidth;
        let h = canvas.height = canvas.offsetHeight;
        
        const particles = [];
        for(let i=0; i<50; i++) {
            particles.push({
                x: Math.random() * w,
                y: Math.random() * h,
                vx: (Math.random() - 0.5) * 0.2,
                vy: (Math.random() - 0.5) * 0.2,
                s: Math.random() * 2
            });
        }

        const animate = () => {
            ctx.clearRect(0,0,w,h);
            ctx.fillStyle = 'rgba(0, 210, 255, 0.1)';
            particles.forEach(p => {
                p.x += p.vx; p.y += p.vy;
                if(p.x < 0) p.x = w; if(p.x > w) p.x = 0;
                if(p.y < 0) p.y = h; if(p.y > h) p.y = 0;
                ctx.fillRect(p.x, p.y, p.s, p.s);
            });
            requestAnimationFrame(animate);
        };
        animate();
    }
}

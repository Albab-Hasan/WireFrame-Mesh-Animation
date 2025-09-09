from manim import *
import numpy as np

class WireframeMeshVisualization(ThreeDScene):
    def construct(self):
        # Set camera orientation for three-quarter view
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES, distance=12)
        
        # Animation parameters
        self.twist_amplitude = ValueTracker(1.5)
        self.wave_frequency = ValueTracker(2.0)
        self.ribbon_width = ValueTracker(0.8)
        self.curvature_intensity = ValueTracker(1.2)
        self.time_param = ValueTracker(0)
        
        # Create the parametric surface
        def parametric_surface(u, v):
            # Get current parameter values
            twist_amp = self.twist_amplitude.get_value()
            wave_freq = self.wave_frequency.get_value()
            width = self.ribbon_width.get_value()
            curve_int = self.curvature_intensity.get_value()
            time_val = self.time_param.get_value()
            
            # Enhanced twisted ribbon surface equation
            twist = twist_amp * np.sin(wave_freq * u + time_val)
            width_mod = width * (1 + 0.3 * np.sin(u * 3))
            height_mod = curve_int * np.cos(u * 1.5) * (1 + 0.2 * v * v)
            
            # Main surface equations
            x = (2 + v * np.cos(u * 0.5 + twist)) * np.cos(u) + \
                0.5 * np.sin(u * wave_freq + time_val * 0.5) * width_mod
            y = height_mod + v * np.sin(u * 0.5 + twist) * 0.5 + \
                0.3 * np.sin(time_val + u * 2) * 0.5
            z = (2 + v * np.cos(u * 0.5 + twist)) * np.sin(u) + \
                0.3 * np.cos(u * wave_freq + time_val * 0.3) * width_mod
            
            return np.array([x, y, z])
        
        # Create surface with wireframe
        surface = Surface(
            parametric_surface,
            u_range=[-PI, PI],
            v_range=[-2, 2],
            resolution=(60, 45),  # Reduced for better performance
            fill_opacity=0,
            stroke_width=1.0,
            stroke_color=DARK_GRAY,
            should_make_jagged=True,  # This creates wireframe effect
        )
        
        # Make it always update based on trackers
        surface.add_updater(
            lambda mob: mob.become(Surface(
                parametric_surface,
                u_range=[-PI, PI],
                v_range=[-2, 2],
                resolution=(60, 45),
                fill_opacity=0,
                stroke_width=1.0,
                stroke_color=DARK_GRAY,
                should_make_jagged=True,
            ))
        )
        
        # Add title (will be 2D overlay)
        title = Text("3D Wireframe Mesh Visualization", font_size=28, color=DARK_GRAY)
        title.to_edge(UP)
        title.add_updater(lambda m: m.to_edge(UP))  # Keep it fixed at top
        
        # Animation sequence
        self.add_fixed_in_frame_mobjects(title)  # This keeps title fixed in 2D
        
        # 1. Initial surface appearance with gentle rotation
        self.play(
            Create(surface),
            run_time=3
        )
        
        # 2. Start ambient rotation
        self.begin_ambient_camera_rotation(rate=0.1)
        
        # 3. Continuous time-based animation with parameter morphing
        self.play(
            self.time_param.animate.set_value(TAU),
            run_time=6
        )
        
        # 4. Morph twist amplitude
        self.play(
            self.twist_amplitude.animate.set_value(3.0),
            run_time=4
        )
        
        self.play(
            self.twist_amplitude.animate.set_value(0.5),
            run_time=4
        )
        
        self.play(
            self.twist_amplitude.animate.set_value(1.5),
            run_time=3
        )
        
        # 5. Morph wave frequency
        self.play(
            self.wave_frequency.animate.set_value(4.0),
            run_time=4
        )
        
        self.play(
            self.wave_frequency.animate.set_value(1.0),
            run_time=4
        )
        
        self.play(
            self.wave_frequency.animate.set_value(2.0),
            run_time=3
        )
        
        # 6. Morph ribbon width and curvature simultaneously
        self.play(
            self.ribbon_width.animate.set_value(1.5),
            self.curvature_intensity.animate.set_value(2.0),
            run_time=4
        )
        
        self.play(
            self.ribbon_width.animate.set_value(0.3),
            self.curvature_intensity.animate.set_value(0.5),
            run_time=4
        )
        
        self.play(
            self.ribbon_width.animate.set_value(0.8),
            self.curvature_intensity.animate.set_value(1.2),
            run_time=3
        )
        
        # 7. Complex morphing sequence with time animation
        self.play(
            self.time_param.animate.set_value(TAU * 2),
            self.twist_amplitude.animate.set_value(2.5),
            self.wave_frequency.animate.set_value(3.0),
            run_time=6
        )
        
        # 8. Camera movement showcase
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=30 * DEGREES, theta=90 * DEGREES, run_time=4)
        self.move_camera(phi=90 * DEGREES, theta=0 * DEGREES, run_time=4)
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, run_time=4)
        
        # 9. Final morphing sequence
        self.begin_ambient_camera_rotation(rate=0.05)
        self.play(
            self.twist_amplitude.animate.set_value(1.8),
            self.wave_frequency.animate.set_value(2.5),
            self.ribbon_width.animate.set_value(1.0),
            self.curvature_intensity.animate.set_value(1.5),
            self.time_param.animate.set_value(TAU * 3),
            run_time=6
        )
        
        # 10. Elegant conclusion
        self.play(
            self.time_param.animate.set_value(TAU * 4),
            run_time=4
        )
        
        self.stop_ambient_camera_rotation()
        self.wait(2)

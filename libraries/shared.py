import math

def convertRGBTo565(r, g, b):
    
    # Ensure the values are within the 0-255 range
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    # Bit-shift the values
    r5 = r >> 3
    g6 = g >> 2
    b5 = b >> 3
    
    # Combine into a 16-bit number
    rgb565 = (r5 << 11) | (g6 << 5) | b5
    return rgb565

def interpolateColor(color_start, color_end, percentage, color_cap=200):
    """
    Interpolates between two RGB colors based on a percentage value and ensures a bright midpoint.
    
    Parameters:
    - color_start: A tuple containing the RGB values of the start color.
    - color_end: A tuple containing the RGB values of the end color.
    - percentage: An integer or float between 0 and 100 representing the interpolation percentage.
    - color_cap: The maximum value for each color component to ensure brightness without exceeding limits.
    
    Returns:
    - A tuple representing the interpolated RGB color, capped at color_cap.
    """
    def capColor(value):
        """Ensure the color component does not exceed color_cap."""
        return min(max(int(value), 0), color_cap)
    
    def interpolateComponent(start, end, percentage):
        """Interpolate a single color component."""
        return start + (end - start) * percentage / 100
    
    r = interpolateComponent(color_start[0], color_end[0], percentage)
    g = interpolateComponent(color_start[1], color_end[1], percentage)
    b = interpolateComponent(color_start[2], color_end[2], percentage)
    
    # Adjusting midpoint to be brighter if needed
    # if percentage == 50:
        # Scale up color components for the midpoint to be as bright as possible
    max_comp = max(r, g, b)
    if max_comp > 0:
        scale_factor = color_cap / max_comp
        r, g, b = (r * scale_factor, g * scale_factor, b * scale_factor)
    
    # Cap the color components to ensure they do not exceed color_cap
    return (capColor(r), capColor(g), capColor(b))

def translateLinearProportion(v, ff, cf, ft, ct):
    proportion = (v - ff) / (cf - ff)
    output = (proportion * (ct - ft)) + ft
    output = max(ft, min(ct, output))
    return output

def clamp(n, n_min, n_max):
    return max(n_min, min(n, n_max))

class PID:
    """ Class representing a PID controller """

    def __init__(self, proportional, integral, derivative):

        # Tuning attributes
        self.proportional = proportional
        self.integral = integral
        self.derivative = derivative

        # Error attributes
        self.previous_error_proportional = 0
        self.previous_error_integral = 0

    def calculate(self, set_point, variable, integral_clamp_max):
        
        # Calculate the proportional value
        error_proportional = set_point - variable

        # Calculate the integral value
        error_integral = clamp(self.previous_error_integral + (error_proportional * self.integral), -integral_clamp_max, integral_clamp_max)

        # Calculate the derivative values
        error_derivative = error_proportional - self.previous_error_proportional

        # Store the current error as the previous error
        self.previous_error_proportional = error_proportional

        # Return the calculated value
        value = (self.proportional * error_proportional) + (self.integral * error_integral) + (self.derivative * error_derivative)
        return value
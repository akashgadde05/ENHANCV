#!/usr/bin/env python3
"""
Create a PNG logo for the Smart ATS Resume Builder
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    def create_logo():
        # Create a 400x400 image with transparent background
        size = (400, 400)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        primary_color = (102, 126, 234)  # #667eea
        secondary_color = (118, 75, 162)  # #764ba2
        accent_color = (240, 147, 251)   # #f093fb
        white = (255, 255, 255)
        
        # Draw main circle background
        center = (200, 200)
        radius = 180
        
        # Create gradient effect by drawing multiple circles
        for i in range(radius, 0, -2):
            # Calculate color interpolation
            ratio = i / radius
            r = int(primary_color[0] * ratio + accent_color[0] * (1 - ratio))
            g = int(primary_color[1] * ratio + accent_color[1] * (1 - ratio))
            b = int(primary_color[2] * ratio + accent_color[2] * (1 - ratio))
            color = (r, g, b, 200)
            
            draw.ellipse([center[0] - i, center[1] - i, center[0] + i, center[1] + i], 
                        fill=color, outline=None)
        
        # Draw document shape
        doc_left = 120
        doc_top = 80
        doc_width = 160
        doc_height = 240
        doc_radius = 20
        
        # Document background
        draw.rounded_rectangle([doc_left, doc_top, doc_left + doc_width, doc_top + doc_height], 
                              radius=doc_radius, fill=white, outline=primary_color, width=4)
        
        # Document lines
        line_start_x = doc_left + 20
        line_end_x = doc_left + doc_width - 20
        line_y_positions = [120, 140, 160, 180, 200, 220, 240, 260]
        
        for y in line_y_positions:
            # Vary line lengths for realistic document look
            end_x = line_end_x - (hash(y) % 40)
            draw.line([line_start_x, y, end_x, y], fill=primary_color, width=3)
        
        # AI brain icon
        brain_center = (240, 120)
        brain_radius = 25
        
        # Brain circle
        draw.ellipse([brain_center[0] - brain_radius, brain_center[1] - brain_radius,
                     brain_center[0] + brain_radius, brain_center[1] + brain_radius],
                    fill=accent_color, outline=white, width=3)
        
        # Brain details (simple dots for neurons)
        brain_dots = [
            (brain_center[0] - 8, brain_center[1] - 8),
            (brain_center[0] + 8, brain_center[1] - 8),
            (brain_center[0], brain_center[1] + 5),
            (brain_center[0] - 5, brain_center[1] + 2),
            (brain_center[0] + 5, brain_center[1] + 2),
        ]
        
        for dot in brain_dots:
            draw.ellipse([dot[0] - 3, dot[1] - 3, dot[0] + 3, dot[1] + 3], fill=white)
        
        # Enhancement sparkles
        sparkle_positions = [
            (80, 160),
            (320, 240),
            (100, 280),
            (300, 140),
        ]
        
        for pos in sparkle_positions:
            # Draw star shape
            star_size = 15
            points = []
            for i in range(10):
                angle = i * 36 * 3.14159 / 180
                if i % 2 == 0:
                    radius = star_size
                else:
                    radius = star_size // 2
                x = pos[0] + radius * (angle ** 0.5) % 2 - 1
                y = pos[1] + radius * (angle ** 0.3) % 2 - 1
                points.append((int(x), int(y)))
            
            # Simple sparkle as diamond
            draw.polygon([
                (pos[0], pos[1] - star_size),
                (pos[0] + star_size, pos[1]),
                (pos[0], pos[1] + star_size),
                (pos[0] - star_size, pos[1])
            ], fill=accent_color)
        
        # Save the image
        img.save('static/images/logo.png', 'PNG')
        print("✅ Logo created successfully: static/images/logo.png")
        
        # Also create a smaller version for navbar
        small_img = img.resize((100, 100), Image.Resampling.LANCZOS)
        small_img.save('static/images/logo-small.png', 'PNG')
        print("✅ Small logo created: static/images/logo-small.png")
        
        return True
        
    if __name__ == "__main__":
        create_logo()
        
except ImportError:
    print("⚠️  Pillow not available. Creating a simple placeholder...")
    
    # Create a simple HTML-based logo placeholder
    placeholder_html = """
    <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #667eea, #764ba2); 
                border-radius: 20px; display: flex; align-items: center; justify-content: center; 
                color: white; font-weight: bold; font-size: 24px;">
        ATS
    </div>
    """
    
    with open('static/images/logo-placeholder.html', 'w') as f:
        f.write(placeholder_html)
    
    print("✅ Logo placeholder created: static/images/logo-placeholder.html")
    print("💡 Install Pillow for better logo: pip install Pillow")
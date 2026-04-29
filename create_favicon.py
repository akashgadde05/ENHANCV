#!/usr/bin/env python3
"""
Create a favicon for the Smart ATS Resume Builder
"""

try:
    from PIL import Image, ImageDraw
    import os
    
    def create_favicon():
        # Create a 32x32 favicon
        size = (32, 32)
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors
        primary_color = (102, 126, 234)  # #667eea
        accent_color = (240, 147, 251)   # #f093fb
        white = (255, 255, 255)
        
        # Draw main circle background
        center = (16, 16)
        radius = 14
        
        # Create gradient effect
        for i in range(radius, 0, -1):
            ratio = i / radius
            r = int(primary_color[0] * ratio + accent_color[0] * (1 - ratio))
            g = int(primary_color[1] * ratio + accent_color[1] * (1 - ratio))
            b = int(primary_color[2] * ratio + accent_color[2] * (1 - ratio))
            color = (r, g, b, 255)
            
            draw.ellipse([center[0] - i, center[1] - i, center[0] + i, center[1] + i], 
                        fill=color)
        
        # Draw simple document icon
        doc_left = 8
        doc_top = 6
        doc_width = 16
        doc_height = 20
        
        # Document background
        draw.rectangle([doc_left, doc_top, doc_left + doc_width, doc_top + doc_height], 
                      fill=white, outline=primary_color, width=1)
        
        # Document lines
        for y in [10, 14, 18, 22]:
            draw.line([doc_left + 2, y, doc_left + doc_width - 2, y], fill=primary_color, width=1)
        
        # Save as ICO file
        img.save('static/favicon.ico', format='ICO', sizes=[(32, 32)])
        print("✅ Favicon created: static/favicon.ico")
        
        # Also save as PNG for modern browsers
        img.save('static/images/favicon.png', 'PNG')
        print("✅ Favicon PNG created: static/images/favicon.png")
        
        return True
        
    if __name__ == "__main__":
        create_favicon()
        
except ImportError:
    print("⚠️  Pillow not available for favicon creation")
    print("💡 Install Pillow: pip install Pillow")
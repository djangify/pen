from django.http import HttpResponsePermanentRedirect
import re

class WordPressRedirectMiddleware:
    """
    Middleware to handle old WordPress URL patterns and redirect them properly
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Pattern-based redirects (regex pattern, target URL)
        self.pattern_redirects = [
            # Plugin/vendor paths - redirect to homepage
            (r'^wp-content/plugins/blockart-blocks/vendor/.*', '/'),
            (r'^wp-content/plugins/blockart-blocks/.*', '/'),
            (r'^wp-content/plugins/.*', '/'),
            
            # WordPress core paths - redirect to homepage
            (r'^wp-content/.*', '/'),
            (r'^wp-includes/.*', '/'),
            (r'^wp-admin/.*', '/'),
            
            # WordPress content structure - map to your Django structure
            (r'^tag/(.+)', '/topics/\\1/'),  # Adjust to your URL structure
            (r'^category/(.+)', '/category/\\1/'),  # Adjust to your URL structure
            
            # Maps and assets - redirect to homepage
            (r'^dist/map/.*', '/'),
            (r'^assets/json/.*', '/'),
            
            # Social elements - redirect to homepage
            (r'^dist/social-inner/.*', '/'),
            
            # Catch any other WordPress-related URLs
            (r'^vendor/.*', '/'),
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = []
        for pattern, target in self.pattern_redirects:
            self.compiled_patterns.append((re.compile(pattern), target))
    
    def __call__(self, request):
        # Extract path from the request (remove leading slash)
        path = request.path.lstrip('/')
        
        # Check for pattern matches
        for pattern, target in self.compiled_patterns:
            match = pattern.match(path)
            if match:
                # If the pattern has capturing groups, use them in the redirect
                if match.groups() and '\\' in target:
                    # Replace \1, \2, etc. with the captured groups
                    for i, group in enumerate(match.groups(), 1):
                        target = target.replace(f'\\{i}', group)
                
                # Use permanent redirects (301) for SEO benefit
                return HttpResponsePermanentRedirect(target)
                
        # If no matches, continue with the regular request
        return self.get_response(request)
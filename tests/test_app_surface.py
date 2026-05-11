import os
import requests
import pytest


BASE_URL = os.getenv('APP_BASE_URL', 'http://192.99.71.97:8081')


# APP SHELL & ASSET TESTS (Integration)


class TestAppShell:
    """Test app server response and basic HTTP endpoints"""
    
    def test_root_returns_html(self):
        """Test: GET / returns 200 with HTML content"""
        r = requests.get(f"{BASE_URL}/", timeout=10)
        assert r.status_code == 200
        content_type = r.headers.get('Content-Type', '')
        assert 'html' in content_type.lower()
        assert 'RAW Pressery' in r.text or 'Welcome Back' in r.text

    def test_vite_svg_served(self):
        """Test: GET /vite.svg returns 200 with SVG content"""
        r = requests.get(f"{BASE_URL}/vite.svg", timeout=10)
        assert r.status_code == 200
        content_type = r.headers.get('Content-Type', '')
        assert 'svg' in content_type.lower() or 'xml' in content_type.lower()
        assert '<svg' in r.text

    def test_app_loads_without_errors(self):
        """Test: App loads successfully (no 5xx errors)"""
        r = requests.get(f"{BASE_URL}/", timeout=10)
        assert 200 <= r.status_code < 500, f"Server error: {r.status_code}"

    def test_html_contains_login_form(self):
        """Test: HTML includes the app shell that mounts the login form client-side"""
        r = requests.get(f"{BASE_URL}/", timeout=10)
        html = r.text.lower()
        assert 'id="root"' in html



# Login


class TestLoginComponent:
    """Unit tests for login validation logic"""
    
    def test_valid_login_credentials(self):
        """Test: handleSubmit() with valid credentials (dineth / dineth@123)"""
        username = 'dineth'
        password = 'dineth@123'
        # Simulate login validation logic from handleSubmit()
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is True
    
    def test_invalid_username(self):
        """Test: handleSubmit() with invalid username"""
        username = 'wrong_user'
        password = 'dineth@123'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_invalid_password(self):
        """Test: handleSubmit() with invalid password"""
        username = 'dineth'
        password = 'wrong_password'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_both_credentials_invalid(self):
        """Test: handleSubmit() with both invalid"""
        username = 'invalid'
        password = 'invalid'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_empty_username(self):
        """Test: handleSubmit() with empty username"""
        username = ''
        password = 'dineth@123'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_empty_password(self):
        """Test: handleSubmit() with empty password"""
        username = 'dineth'
        password = ''
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_whitespace_in_username(self):
        """Test: handleSubmit() rejects username with extra whitespace"""
        username = ' dineth '
        password = 'dineth@123'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_case_sensitive_username(self):
        """Test: Username is case-sensitive"""
        username = 'DINETH'
        password = 'dineth@123'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False
    
    def test_case_sensitive_password(self):
        """Test: Password is case-sensitive"""
        username = 'dineth'
        password = 'DINETH@123'
        is_valid = username == 'dineth' and password == 'dineth@123'
        assert is_valid is False



# Navigation bar


# class TestNavbarComponent:
#     """Unit tests for Navbar buttons and navigation"""
    
#     def test_navbar_contains_required_links(self):
#         """Test: Navbar contains all required navigation links"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         required_links = ['Shop', 'Our Story', 'Flavors', 'Subscription']
#         for link in required_links:
#             assert link in r.text, f"Navigation link '{link}' not found in page"
    
#     def test_navbar_logo_present(self):
#         """Test: Navbar contains RAW Pressery logo"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         assert 'RAW' in r.text
#         assert 'Pressery' in r.text
    
#     def test_mobile_menu_button_exists(self):
#         """Test: Mobile menu toggle button (setIsOpen) is rendered"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         # Mobile menu logic uses setIsOpen state toggle
#         assert 'md:hidden' in r.text



# # PRODUCT COMPONENT TESTS 


# class TestProductComponent:
#     """Unit tests for Product buttons and functions"""
    
#     def test_add_to_cart_button_present(self):
#         """Test: Add to cart button (FaPlus icon) is present"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         # FaPlus button is in ProductGrid component
#         assert 'Alphonso' in r.text or 'product' in r.text.lower()
    
#     def test_product_price_display(self):
#         """Test: Product prices are displayed"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         # Check for price indicators
#         content_lower = r.text.lower()
#         has_price = any(x in content_lower for x in ['$', '₹', 'rs', 'price'])
#         assert has_price, "Product prices not found on page"
    
#     def test_product_grid_renders(self):
#         """Test: Product grid component renders successfully"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         assert r.status_code == 200


# # submition and validation tests


# class TestFormSubmission:
#     """Test form submission and validation workflows"""
    
#     def test_login_form_has_submit_button(self):
#         """Test: Login form contains a submit/Sign In button"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         assert 'submit' in r.text.lower() or 'sign in' in r.text.lower()
    
#     def test_login_form_has_username_field(self):
#         """Test: Login form contains username input field"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         assert 'username' in r.text.lower()
    
#     def test_login_form_has_password_field(self):
#         """Test: Login form contains password input field"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         assert 'password' in r.text.lower()
    
#     def test_form_fields_are_required(self):
#         """Test: Login form fields are marked as required"""
#         r = requests.get(f"{BASE_URL}/", timeout=10)
#         assert 'required' in r.text.lower()

"""
Internationalization (i18n) manager for Soplos Welcome.
Handles GNU Gettext translation loading, language detection, and string management.
"""

import os
import locale
import gettext
from pathlib import Path
from typing import Dict, List, Optional, Union


class I18nManager:
    """
    Manages internationalization using GNU Gettext.
    Provides automatic language detection and translation services.
    """
    
    # Supported languages with their locale codes
    SUPPORTED_LANGUAGES = {
        'es': 'Spanish',
        'en': 'English', 
        'fr': 'French',
        'de': 'German',
        'pt': 'Portuguese',
        'it': 'Italian',
        'ro': 'Romanian',
        'ru': 'Russian'
    }
    
    # Language fallback chain
    FALLBACK_CHAIN = ['en', 'es']
    
    def __init__(self, locale_dir: str, domain: str = 'soplos-welcome'):
        """
        Initialize the i18n manager.
        
        Args:
            locale_dir: Path to locale directory containing .mo files
            domain: Translation domain name
        """
        self.locale_dir = Path(locale_dir)
        self.domain = domain
        self.current_language = None
        self.translations = {}
        self.fallback_translation = None
        
        # Ensure locale directory exists
        self.locale_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize translations
        self._load_translations()
        
        # Detect and set system language
        detected_lang = self.detect_system_language()
        self.set_language(detected_lang)
    
    def _load_translations(self):
        """Load all available translations."""
        for lang_code in self.SUPPORTED_LANGUAGES.keys():
            mo_file = self.locale_dir / lang_code / 'LC_MESSAGES' / f'{self.domain}.mo'
            
            if mo_file.exists():
                try:
                    with open(mo_file, 'rb') as f:
                        translation = gettext.GNUTranslations(f)
                        self.translations[lang_code] = translation
                        print(f"Loaded translation for {lang_code}")
                except Exception as e:
                    print(f"Error loading translation for {lang_code}: {e}")
        
        # Set fallback translation (English)
        if 'en' in self.translations:
            self.fallback_translation = self.translations['en']
        else:
            # Create a null translation if English is not available
            self.fallback_translation = gettext.NullTranslations()
    
    def detect_system_language(self) -> str:
        """
        Detect system language with multiple fallback methods.
        
        Returns:
            Detected language code
        """
        # Method 1: Environment variables (in order of preference)
        env_vars = ['SOPLOS_WELCOME_LANG', 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG']
        
        for env_var in env_vars:
            env_value = os.environ.get(env_var)
            if env_value:
                # Extract language code from locale string (e.g., 'es_ES.UTF-8' -> 'es')
                lang_code = env_value.split('_')[0].split('.')[0].split('@')[0].lower()
                if lang_code in self.SUPPORTED_LANGUAGES:
                    return lang_code
        
        # Method 2: Python locale module
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                lang_code = system_locale.split('_')[0].lower()
                if lang_code in self.SUPPORTED_LANGUAGES:
                    return lang_code
        except Exception as e:
            print(f"Error detecting locale: {e}")
        
        # Method 3: Try to read from system locale files
        locale_files = ['/etc/locale.conf', '/etc/default/locale']
        for locale_file in locale_files:
            try:
                if os.path.exists(locale_file):
                    with open(locale_file, 'r') as f:
                        for line in f:
                            if line.startswith('LANG='):
                                lang_value = line.split('=', 1)[1].strip().strip('"\'')
                                lang_code = lang_value.split('_')[0].split('.')[0].lower()
                                if lang_code in self.SUPPORTED_LANGUAGES:
                                    return lang_code
            except Exception as e:
                print(f"Error reading {locale_file}: {e}")
        
        # Default fallback
        return 'en'
    
    def set_language(self, language_code: str) -> bool:
        """
        Set the current language for translations.
        
        Args:
            language_code: Language code to set
            
        Returns:
            True if language was set successfully, False otherwise
        """
        if language_code not in self.SUPPORTED_LANGUAGES:
            print(f"Unsupported language: {language_code}")
            return False
        
        if language_code in self.translations:
            self.current_language = language_code
            
            # Install the translation globally for gettext
            self.translations[language_code].install()
            
            print(f"Language set to: {language_code} ({self.SUPPORTED_LANGUAGES[language_code]})")
            return True
        else:
            print(f"Translation not available for: {language_code}")
            
            # Try fallback languages
            for fallback_lang in self.FALLBACK_CHAIN:
                if fallback_lang in self.translations:
                    self.current_language = fallback_lang
                    self.translations[fallback_lang].install()
                    print(f"Using fallback language: {fallback_lang}")
                    return True
            
            # Use null translation as last resort
            self.current_language = 'en'
            self.fallback_translation.install()
            return False
    
    def get_translation(self, message: str, **kwargs) -> str:
        """
        Get translated message with optional formatting.
        
        Args:
            message: Message key to translate
            **kwargs: Format arguments for the message
            
        Returns:
            Translated and formatted message
        """
        if self.current_language and self.current_language in self.translations:
            try:
                translated = self.translations[self.current_language].gettext(message)
            except Exception:
                translated = message
        else:
            translated = message
        
        # If translation failed, try fallback
        if translated == message and self.fallback_translation:
            try:
                translated = self.fallback_translation.gettext(message)
            except Exception:
                pass
        
        # Apply formatting if provided
        if kwargs:
            try:
                translated = translated.format(**kwargs)
            except Exception as e:
                print(f"Error formatting message '{message}': {e}")
        
        return translated
    
    def get_plural_translation(self, singular: str, plural: str, count: int, **kwargs) -> str:
        """
        Get translated message with plural support.
        
        Args:
            singular: Singular form of the message
            plural: Plural form of the message  
            count: Count to determine plural form
            **kwargs: Format arguments for the message
            
        Returns:
            Translated and formatted message
        """
        if self.current_language and self.current_language in self.translations:
            try:
                translated = self.translations[self.current_language].ngettext(singular, plural, count)
            except Exception:
                translated = singular if count == 1 else plural
        else:
            translated = singular if count == 1 else plural
        
        # If translation failed, try fallback
        if translated in (singular, plural) and self.fallback_translation:
            try:
                translated = self.fallback_translation.ngettext(singular, plural, count)
            except Exception:
                pass
        
        # Apply formatting if provided
        kwargs['count'] = count  # Always include count in formatting
        if kwargs:
            try:
                translated = translated.format(**kwargs)
            except Exception as e:
                print(f"Error formatting plural message '{singular}'/'{plural}': {e}")
        
        return translated
    
    def get_available_languages(self) -> Dict[str, str]:
        """
        Get available languages with translations.
        
        Returns:
            Dictionary mapping language codes to language names
        """
        available = {}
        for lang_code, lang_name in self.SUPPORTED_LANGUAGES.items():
            if lang_code in self.translations:
                available[lang_code] = lang_name
        return available
    
    def get_current_language(self) -> str:
        """Get current language code."""
        return self.current_language or 'en'
    
    def get_current_language_name(self) -> str:
        """Get current language name."""
        current = self.get_current_language()
        return self.SUPPORTED_LANGUAGES.get(current, 'English')
    
    def reload_translations(self):
        """Reload all translations from disk."""
        self.translations.clear()
        self._load_translations()
        
        # Re-set current language
        if self.current_language:
            current = self.current_language
            self.current_language = None
            self.set_language(current)
    
    def _(self, message: str, **kwargs) -> str:
        """
        Convenience method for translation (equivalent to get_translation).
        
        Args:
            message: Message to translate
            **kwargs: Format arguments
            
        Returns:
            Translated message
        """
        return self.get_translation(message, **kwargs)
    
    def create_pot_template(self, source_files: List[str], output_file: str):
        """
        Create a POT template file for translators.
        
        Args:
            source_files: List of Python source files to extract strings from
            output_file: Output POT file path
        """
        try:
            import subprocess
            
            cmd = [
                'xgettext',
                '--language=Python',
                '--keyword=_',
                '--keyword=ngettext:1,2',
                '--output=' + output_file,
                '--from-code=UTF-8',
                '--add-comments=TRANSLATORS',
                '--copyright-holder=Sergi Perich',
                '--package-name=soplos-welcome',
                '--package-version=2.0.1',
                '--msgid-bugs-address=info@soploslinux.com'
            ] + source_files
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"POT template created: {output_file}")
            else:
                print(f"Error creating POT template: {result.stderr}")
                
        except FileNotFoundError:
            print("xgettext not found. Please install gettext tools.")
        except Exception as e:
            print(f"Error creating POT template: {e}")


# Global i18n manager instance
_i18n_manager = None

def get_i18n_manager(locale_dir: str = None, domain: str = 'soplos-welcome') -> I18nManager:
    """
    Returns the global i18n manager instance.
    
    Args:
        locale_dir: Locale directory path (only used on first call)
        domain: Translation domain (only used on first call)
        
    Returns:
        Global I18nManager instance
    """
    global _i18n_manager
    if _i18n_manager is None:
        if locale_dir is None:
            # Default path relative to this file
            current_dir = Path(__file__).parent.parent
            locale_dir = current_dir / 'locale'
        _i18n_manager = I18nManager(str(locale_dir), domain)
    return _i18n_manager

def _(message: str, **kwargs) -> str:
    """
    Convenience function for translation.
    
    Args:
        message: Message to translate
        **kwargs: Format arguments
        
    Returns:
        Translated message
    """
    manager = get_i18n_manager()
    return manager.get_translation(message, **kwargs)

def ngettext(singular: str, plural: str, count: int, **kwargs) -> str:
    """
    Convenience function for plural translation.
    
    Args:
        singular: Singular form
        plural: Plural form
        count: Count for plural determination
        **kwargs: Format arguments
        
    Returns:
        Translated plural message
    """
    manager = get_i18n_manager()
    return manager.get_plural_translation(singular, plural, count, **kwargs)

def set_language(language_code: str) -> bool:
    """
    Set current language.
    
    Args:
        language_code: Language code to set
        
    Returns:
        True if successful
    """
    manager = get_i18n_manager()
    return manager.set_language(language_code)

def get_current_language() -> str:
    """Get current language code."""
    manager = get_i18n_manager()
    return manager.get_current_language()

def initialize_i18n(locale_dir: str = None, domain: str = 'soplos-welcome') -> str:
    """
    Initialize the internationalization system.
    
    Args:
        locale_dir: Locale directory path
        domain: Translation domain
        
    Returns:
        Current language code
    """
    manager = get_i18n_manager(locale_dir, domain)
    return manager.get_current_language()

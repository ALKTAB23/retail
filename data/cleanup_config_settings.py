# -*- coding: utf-8 -*-
"""
Script to clean up config settings issues after upgrade
Run this in Odoo shell:
  python3 odoo-bin shell -d your_database -c /etc/odoo.conf --shell-interface=ipython
  exec(open('/path/to/this/file.py').read())
"""

import logging
_logger = logging.getLogger(__name__)

def cleanup_pos_config_settings():
    """Clean up corrupted POS config settings after upgrade"""
    
    try:
        # Clean up res.config.settings records with invalid values
        config_settings = env['res.config.settings'].sudo()
        
        # Remove any existing transient records that might have bad data
        invalid_settings = config_settings.search([])
        if invalid_settings:
            _logger.info(f"Removing {len(invalid_settings)} potentially corrupted config settings")
            invalid_settings.unlink()
        
        # Check for POS configs with invalid category references
        pos_configs = env['pos.config'].sudo().search([])
        
        for config in pos_configs:
            try:
                # Test if the category field is accessible
                category = config.sh_carry_bag_category
                if category and not category.exists():
                    _logger.info(f"Clearing invalid category for POS config {config.name}")
                    config.sh_carry_bag_category = False
                    
                # Test the pos_sh_carry_bag_category field too
                pos_category = config.pos_sh_carry_bag_category  
                if pos_category and not pos_category.exists():
                    _logger.info(f"Clearing invalid pos category for POS config {config.name}")
                    config.pos_sh_carry_bag_category = False
                    
            except Exception as e:
                _logger.warning(f"Error checking POS config {config.name}: {e}")
                # Clear problematic fields
                config.write({
                    'sh_carry_bag_category': False,
                    'pos_sh_carry_bag_category': False
                })
        
        env.cr.commit()
        _logger.info("POS config cleanup completed successfully")
        return True
        
    except Exception as e:
        _logger.error(f"Error during cleanup: {e}")
        env.cr.rollback()
        return False

if __name__ == '__main__':
    # Run the cleanup
    result = cleanup_pos_config_settings()
    print(f"Cleanup result: {result}")
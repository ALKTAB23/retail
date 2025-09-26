# -*- coding: utf-8 -*-
"""
Post-migration script for Odoo 18.0
Fixes config settings field type conflicts
"""

import logging
from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    """Fix config settings after migration to Odoo 18"""
    _logger.info("Starting post-migration fixes for sh_pos_all_in_one_retail...")
    
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        try:
            # Clear any invalid transient config settings
            _logger.info("Cleaning up res.config.settings records...")
            config_settings = env['res.config.settings'].sudo().search([])
            if config_settings:
                config_settings.unlink()
                _logger.info(f"Removed {len(config_settings)} config settings records")
            
            # Fix POS config category fields
            _logger.info("Fixing POS config category fields...")
            pos_configs = env['pos.config'].sudo().search([])
            
            for config in pos_configs:
                try:
                    # Reset category fields that might have wrong model references
                    updates = {}
                    
                    # Check and reset sh_carry_bag_category if it's invalid
                    try:
                        if hasattr(config, 'sh_carry_bag_category') and config.sh_carry_bag_category:
                            # Try to access the field to see if it's valid
                            config.sh_carry_bag_category.name
                    except Exception:
                        _logger.info(f"Resetting sh_carry_bag_category for config {config.name}")
                        updates['sh_carry_bag_category'] = False
                    
                    # Check and reset pos_sh_carry_bag_category if it's invalid  
                    try:
                        if hasattr(config, 'pos_sh_carry_bag_category') and config.pos_sh_carry_bag_category:
                            config.pos_sh_carry_bag_category.name
                    except Exception:
                        _logger.info(f"Resetting pos_sh_carry_bag_category for config {config.name}")
                        updates['pos_sh_carry_bag_category'] = False
                    
                    if updates:
                        config.write(updates)
                        
                except Exception as e:
                    _logger.warning(f"Error fixing config {config.name}: {e}")
                    # Force reset both fields in case of any error
                    try:
                        config.write({
                            'sh_carry_bag_category': False,
                            'pos_sh_carry_bag_category': False
                        })
                    except Exception as e2:
                        _logger.error(f"Could not reset config {config.name}: {e2}")
            
            # Force update module registry
            env.registry.setup_models(cr)
            
            _logger.info("Post-migration fixes completed successfully")
            
        except Exception as e:
            _logger.error(f"Error during post-migration: {e}")
            # Don't raise the error to prevent migration failure
            pass
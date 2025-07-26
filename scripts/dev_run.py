#!/usr/bin/env python3
"""
Development script for running the Crystal HR Automation package.
This script is not included in the installed package.
"""
import argparse
import logging
import os
import sys
from pathlib import Path

# Add package root to Python path
PACKAGE_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PACKAGE_ROOT))

def main():
    """Run the package with command-line arguments."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Development runner for Crystal HR Automation')
    parser.add_argument('command', choices=['punch', 'config'], 
                       help='Command to run')
    parser.add_argument('action', nargs='?', 
                       help='Action for the command')
    parser.add_argument('--debug', action='store_true', 
                       help='Enable debug logging')
    parser.add_argument('--config', type=Path, 
                       help='Path to config file')
    parser.add_argument('--delay', type=int, 
                       help='Delay in minutes before performing the action')
    
    # Parse arguments
    args, extra_args = parser.parse_known_args()
    
    # Set up logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('dev_run.log', encoding='utf-8')
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Crystal HR Automation (dev mode)")
    
    # Prepare command line arguments for the actual package
    cmd_args = [args.command]
    
    if args.action:
        cmd_args.append(args.action)
    
    if args.delay is not None:
        cmd_args.extend(['--delay', str(args.delay)])
    
    if args.config:
        cmd_args.extend(['--config', str(args.config)])
    
    if args.debug:
        cmd_args.append('--debug')
    
    # Add any extra arguments
    cmd_args.extend(extra_args)
    
    # Import and run the main CLI
    from rajnish_dc_crystal.cli import main as cli_main
    
    # Set sys.argv to our constructed arguments
    sys.argv = [sys.argv[0]] + cmd_args
    
    # Run the CLI
    return cli_main()

if __name__ == "__main__":
    sys.exit(main())




dow={'monday': {}, 
	'tuesday': {}, 
	'wednesday': {}, 
	'thursday': {}, 
	'friday': {}, 
	'saturday': {}, 
	'sunday': {}
	}
	
requiredProperties={'network_name': ('<Name> - Required. Name of the network', 'str'),
	'channel_number': ('<Number> - Required. Channel number. ex. 6', 'int', [1,99]),
	'content_dir': ('<Name> - Directory containing video content files', 'str')
	}
	
requiredProperties.update(dow)
	
optionalProperties={
	'day_templates': ('<Name list> - Reusable day configurations', 'str'), 
	'slot_overrides': ('<Name list> - Define named override sets for reuse across multiple time slots', 'str'),
	'tag_overrides': (' <Name list> - Define a named override for a tag', 'str'),
	'network_long_name': ('<Name> - Descriptive Name', 'str'),
	'network_type': ('<standard, web, loop, guide, streaming>', ['standard', 'web', 'loop', 'guide', 'streaming']),
	'break_duration': ('<Number> - Duration of commercial breaks in seconds', 'int'),
	'break_strategy': ('<standard, center, end> - When to insert commercial breaks', ['standard', 'center', 'end']),
	'schedule_increment': ('<Number> - Time slot increment in minutes. 0 (continuous), 30, 60, etc.', 'int'),
	'schedule_offset': ('<Number> - Offset in minutes from start of hour for showtimes', 'int'),
	'commercial_free': ('<False, True> - Whether channel has commercials', [False, True]),
	'commercial_dir': ('<Name> Directory containing commercial videos', 'str'), 
	'bump_dir': ('<Name> - Directory containing bump/interstitial videos', 'str'), 
	'clip_shows': ('<Name list> - List of clip show configurations', 'str'), 
	'sign_off_video': ('<Name> - Video played during sign-off event', 'str'), 
	'off_air_video': ('<Name> - Video/pattern shown when off-air', 'str'),
	'standby_image': ('<Name> - Image shown when channel is on standby', 'str'), 
	'be_right_back_media': ('<Name> - Image/video shown during brief interruptions', 'str'), 
	'autobump': ('<Config> - Automatically generate bump videos with metadata', 'config'),
	'hidden': ('<True, False> - Hide channel from guide listings', [True, False]),
	'fallback_tag': ('<Name> - Tag/folder used when no content is found for a scheduled slot', 'str'), 
	'runtime_dir': ('<Name> - Depricated - Directory for runtime data (schedules, catalogs)', 'str') 
	}

overrideProperties={'start_bump': ('<Name> - Path to bump video before content', 'str'),
	'end_bump': ('<Name> - Path to bump video after content', 'str'), 
	'bump_dir': ('<Name> - Directory to override bump directory for this slot', 'str'), 
	'commercial_dir': ('<Name> - Directory to override commercial videos for this slot', 'str'),
	'break_strategy': ('<standard, center, end> - When to insert commercial breaks', ['standard', 'center', 'end']),
	'sequence': ('<Name> - Allows playing episodes in order from a specific range', 'str'),
	'sequence_start': ('<Number> - Starting point. ex. .3', 'float', [0,1]),
	'sequence_end': ('<Number> - Ending point. ex. 0.6', 'float', [0,1]),
	'schedule_increment': ('<Number> - Time slot increment in minutes. 0 (continuous), 30, 60, etc.', 'int'),
	'random_tags': ('<True, False> - Randomly selects one tag from the array for each scheduling operation', [True, False]),
	'marathon': ('<Config> - Trigger probabilistic multi-episode marathons', 'config'),
	'video_scramble_fx': ('<horizontal_line, diagonal_lines, static_overlay, pixel_block, color_inversion, severe_noise, wavy, random_block, chunky_scramble> - Apply preset scrambling effect', ['horizontal_line', 'diagonal_lines', 'static_overlay', 'pixel_block', 'color_inversion', 'severe_noise', 'wavy', 'random_block', 'chunky_scramble'])
	}

tagOverrideProperties=overrideProperties
		
slotProperties={'tags': ('<Name> - Content tag(s) to select from catalog', 'str'),
	'event': ('<signoff> - Special event', ['signoff']),
	'continued': ('<True> - Inherit the previous hour\'s tags (applies tag smoothing)', [True])
	} 
	
slotProperties.update(overrideProperties)

expandCollapse={'Expand &Morning': (6,10),
	'Expand &Day': (10,18), 
	'Expand &Prime': (18, 23), 
	'Expand &Late': (0, 2),
	'Expand &Overnight': (2,6),
	'Expand &All': (0, 24), 
	'C&ollapse All': (0, 24, True)
	}

autobumpRequired={
	'title': ('<Name> - The name for the autobump', 'str')
	}
	
autobumpOptional={
	'subtitle': ('<Name> - Subtitle', 'str'),
	'variation': ('<retro, corporate, modern, terminal> - Visual style variant', ['retro', 'corporate', 'modern', 'terminal']),
	'detail1': ('<Name> - Line 1 of details', 'str'),
	'detail2': ('<Name> - Line 2 of details', 'str'),
	'detail3': ('<Name> - Line 3 of details', 'str'),
	'bg_color':('<Name> - Background color (hex)', 'str'),
	'fg_color': ('<Name> - Text color (hex)', 'str'),
	'bg': ('<Name> - Background image URL. ex. background.jpg', 'str'),
	'css':('<Name> - Custom CSS file', 'str'),
	'next_network': ('<Name> - Show upcoming programs. ex. "nbc", "mtv", "espn"', 'str'),
	'duration': ('<Number> - Auto-hide after seconds', 'int'),
	'bg_music': ('<Name> - Music that plays with the bump. ex. logo1.mp3', 'str'),
	'strategy': ('<both, start, end> - When the bump will occur during the time slot', ['both', 'start', 'end'])
}

autobump=autobumpRequired| autobumpOptional

marathon={ 
	'chance':('<Number> - Probability (0.0 to 1.0) of marathon occurring', 'float', [0,1]), 
	'count': ('<Number> - Number of episodes to play consecutively', 'int')
}






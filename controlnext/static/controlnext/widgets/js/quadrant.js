// Quadrant widget 
(function() {      

	$.widget('elicit.quadrant', {
	    options: {	    	
	    	activequadrant: 0,      
			dot: [{doty: 0, doty: 0}],            
	    },
	    
	    _create: function () {
	        this._setOptions({
	            'activequadrant': this.options.activequadrant,
	            'dot':  this.options.dot            
	        });	                                     
	    },    
	    
	    _destroy: function () {        
	        this.element.empty();
	    },
	    
	    _setOption: function (key, value) {
	        var self = this,
	        prev = this.options[key],
	        fnMap = {
	          'activequadrant': function () {
	            activateQuadrant(value, self);
	            createDot(value, self);
	          },
	          'dot': function () {
	            createDot(value, self);
	          }          
	        };
	        
	        // base
	        this._super(key, value);
	        
	        if (key in fnMap) {
	            fnMap[key]();
	            
	            // Fire event
	            this._triggerOptionChanged(key, prev, value);
	        }
	    },
	    
	    _triggerOptionChanged: function (optionKey, previousValue, currentValue) {
	        this._trigger('setOption', {type: 'setOption'}, {
	            option: optionKey,
	            previous: previousValue,
	            current: currentValue
	        });   
	    }
	});
	
	
	function activateQuadrant(activequadrant, widget) {   
	   
	    // Deactivate all quadrants       
	    quadrantparts = widget.element.find('#quadrant-1, #quadrant-2, #quadrant-3, #quadrant-4')
	        .removeClass('active');
        
		// Activate chosen quadrant	
	    quadrantparts.eq(activequadrant-1).addClass('active');
	}
	
	function createDot(dot, widget) {
	
//		console.log(widget.options.dot[0].doty);
		quadrantdot = widget.element.find('#quadrant-dot');
		
		if((widget.options.dot[0].doty < 0) || (widget.options.dot[0].dotx < 0)) {
			quadrantdot.css('display', 'none');
		}
		else {
			     
		    quadrantdot.css('display', 'block');
			dotradius = (quadrantdot.width()/2);          
		     
		    quadrantdot.css({
		        'bottom':'auto',       
		        'right':'auto'        
		    });
		        
		    quadrantparts = widget.element.find('#quadrant-1, #quadrant-2, #quadrant-3, #quadrant-4');
		    quadrantparts.eq(widget.options.activequadrant-1).append(quadrantdot);
		     
		    quadrantheight = $('#quadrant-1').height();
		    quadrantwidth = $('#quadrant-1').width();
		     
		    $.each(dot, function (idx, d) {  
		    
		        quadrantdot.css({
		            'top': -(quadrantheight/100*dotradius) + d.doty + '%',
		            'left': -(quadrantwidth/100*dotradius) + d.dotx + '%'
		        });
		    });
		}
	}
	
})();	
// Actuele waterstand widget
(function() { 
       
	$.widget('elicit.actualwater', {
	    options: {
	      actualwater: 0
	    },
	    
	    _create: function () {
	        this._setOptions({
	            'actualwater': this.options.actualwater
	        });                                               
	    },    
	    
	    _destroy: function () {        
	        this.element.empty();
	    },
	    
	    _setOption: function (key, value) {
	        var self = this,
	        prev = this.options[key],
	        fnMap = {
	          'actualwater': function () {
	            drawLevel(value, self);
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
	
	function drawLevel(level, widget) {      
	    widget.element.find('.actual').css({'height':level+'%'});
	    widget.element.find('.actuallabel').css({'bottom':level+'%'}); 	    
	}

})();
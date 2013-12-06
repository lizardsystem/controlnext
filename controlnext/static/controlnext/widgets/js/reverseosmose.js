// Reverse Osmose widget       
(function() { 
	
	$.widget('elicit.reverseosmose', {
		
	    options: {
	    	border: showtoday(),     	
			rangestart: showlastweek(),
			rangeend: shownextmonth(),
			rson: showlastmonth(),
			rsoff: shownextmonth(),
            labeltxt: "Reverse osmose" ,
            filltxt: "Ro aan"
	    },
	    
	    _create: function () {
        
            this.element.append('<div class="elicit-reverse-range"><div class="elicit-reverse-fill"></div><div class="elicit-reverse-label"><span></span></div></div>');
                
        
	        this._setOptions({
		        'border': this.options.border,
				'rangestart': this.options.rangestart,
				'rangeend': this.options.rangeend,		
	            'rson': this.options.rson,
	            'rsoff': this.options.rsoff,
                'labeltxt': this.options.labeltxt,
	            'filltxt': this.options.filltxt    
	        });                                               
	    },    
	    
	    _destroy: function () {        
	        this.element.empty();
	    },
	    
	    _setOption: function (key, value) {
	        var self = this,
	        prev = this.options[key],
	        fnMap = {
		      'border': function () {
				 drawOsmose(self); 
	          },
	          'rangestart': function () {
				 drawOsmose(self); 
	          },
	          'rangeend': function () {
				 drawOsmose(self); 
	          },
	          'rson': function () {
				 drawOsmose(self); 
	          },
	          'rsoff': function () {
				 drawOsmose(self);
	          },
	          'labeltxt': function () {
				 setLabel(value, self);
	          },
	          'filltxt': function () {
				 setFill(value, self);
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
	
	function drawBorder(total, widget) {		
		// Get the time difference of today and the start of the range
		var difference = widget.options.border.getTime() - widget.options.rangestart.getTime();
		widget.element.find('.elicit-reverse-label').css({'width':(difference / total*100)+'%'});		
	}
	
    function drawReverserange(total, widget) {
    
        // Get the time difference of the reverse osmose start and the start of the range                                                                                            
        var difference = widget.options.rson.getTime() - widget.options.rangestart.getTime();
        //console.log(difference/total*100);
        
        var rsfill = widget.options.rsoff.getTime() - widget.options.rson.getTime();
        //console.log(rsfill/total*100);
        
        widget.element.find('.elicit-reverse-fill').css({'margin-left':(difference / total*100)+'%'});
        widget.element.find('.elicit-reverse-fill').css({'width':(rsfill / total*100)+'%'});        
    }
    
	function drawOsmose(widget) { 
	    
        // Determine if values are correct        
        if(widget.options.rangestart.getTime() > widget.options.rangeend.getTime())
        {
            throw ('Range start must be before range end');                 
        }
        
        if(widget.options.border.getTime() < widget.options.rangestart.getTime())
        {
            throw ('Border of today '+ widget.options.border +' has an earlier timestamp compare to the start of the range: ' + widget.options.rangestart);                 
        }
        
        if(widget.options.border.getTime() > widget.options.rangeend.getTime())
        {
            throw ('Border of today '+ widget.options.border +' has a later timestamp compare to the end of the range: ' + widget.options.rangeend);                 
        }
        
        if(widget.options.rson.getTime() > widget.options.rsoff.getTime())
        {
            throw ('Osmose rson time must start before rsoff');                 
        }
          
        if(widget.options.rson.getTime() <  widget.options.rangestart.getTime())
        {
            widget._setOption('rson',widget.options.rangestart);
        } 
        
        if(widget.options.rsoff.getTime() >  widget.options.rangeend.getTime())
        {              
            widget._setOption('rsoff',widget.options.rangeend); 
        }
            
        // Determine total time of range. This is 100% time.                        		
        var total =	widget.options.rangeend.getTime() - widget.options.rangestart.getTime();
        
		// Draw the label from start to border
		drawBorder(total,widget);
		
        // Draw the reverse osmose perio
        drawReverserange(total,widget);        
	}
    
    function setLabel(text, widget) {
        widget.element.find('.elicit-reverse-label span').html(text);
    }
    
    function setFill(text, widget) {
        widget.element.find('.elicit-reverse-fill').html(text);
    }
    
		
	function showtoday() {
		var d = new Date();

		return d;
	}
	
	function shownextmonth() {
		d = new Date();
		d.setDate(d.getDate() + 28);	
		return d;
	}
	
	function showlastweek() {
		d = new Date();
		d.setDate(d.getDate() - 7);
		return d;		
	}
    
    function showlastmonth() {
		d = new Date();
		d.setDate(d.getDate() - 28);
		return d;		
	}
    
    function shownextweek() {
		d = new Date();
		d.setDate(d.getDate() + 7);
		return d;		
	}
	
	function mydateformat(date) {
		month 	= date.getMonth()+1;
		day 	= date.getDate();		
		
		return date.getFullYear() + '/' +
	    	((''+month).length<2 ? '0' : '') + month + '/' +
			((''+day).length<2 ? '0' : '') + day;	
	}

})();
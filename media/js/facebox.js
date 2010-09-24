/*
 * Facebox (for jQuery)
 * version: 1.2 (05/05/2008)
 * @requires jQuery v1.2 or later
 *
 * Examples at http://famspam.com/facebox/
 *
 * Licensed under the MIT:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Copyright 2007, 2008 Chris Wanstrath [ chris@ozmm.org ]
 *
 * Usage:
 *  
 *  jQuery(document).ready(function() {
 *    jQuery('a[rel*=facebox]').facebox() 
 *  })
 *
 *  <a href="#terms" rel="facebox">Terms</a>
 *    Loads the #terms div in the box
 *
 *  <a href="terms.html" rel="facebox">Terms</a>
 *    Loads the terms.html page in the box
 *
 *  <a href="terms.png" rel="facebox">Terms</a>
 *    Loads the terms.png image in the box
 *
 *
 *  You can also use it programmatically:
 * 
 *    jQuery.facebox('some html')
 *
 *  The above will open a facebox with "some html" as the content.
 *    
 *    jQuery.facebox(function($) { 
 *      $.get('blah.html', function(data) { $.facebox(data) })
 *    })
 *
 *  The above will show a loading screen before the passed function is called,
 *  allowing for a better ajaxy experience.
 *
 *  The facebox function can also display an ajax page or image:
 *  
 *    jQuery.facebox({ ajax: 'remote.html' })
 *    jQuery.facebox({ image: 'dude.jpg' })
 *
 *  Want to close the facebox?  Trigger the 'close.facebox' document event:
 *
 *    jQuery(document).trigger('close.facebox')
 *
 *  Facebox also has a bunch of other hooks:
 *
 *    loading.facebox
 *    beforeReveal.facebox
 *    reveal.facebox (aliased as 'afterReveal.facebox')
 *    init.facebox
 *
 *  Simply bind a function to any of these hooks:
 *
 *   $(document).bind('reveal.facebox', function() { ...stuff to do after the facebox and contents are revealed... })
 *
 */
(function(f){f.facebox=function(m,l){f.facebox.loading();if(m.ajax){g(m.ajax)}else{if(m.image){c(m.image)}else{if(m.div){j(m.div)}else{if(f.isFunction(m)){m.call(f)}else{f.facebox.reveal(m,l)}}}}};f.extend(f.facebox,{settings:{opacity:0,overlay:true,loadingImage:"/media/images/loading.gif",closeImage:"/media/images/closelabel.gif",imageTypes:["png","jpg","jpeg","gif"],faceboxHtml:'    <div id="facebox" style="display:none;">       <div class="popup">         <table>           <tbody>             <tr>               <td class="tl"/><td class="b"/><td class="tr"/>             </tr>             <tr>               <td class="b"/>               <td class="body">                 <div class="content">                 </div>                 <div class="footer">                   <a href="#" class="close">                     <img src="/media/images/closelabel.gif" title="close" class="close_image" />                   </a>                 </div>               </td>               <td class="b"/>             </tr>             <tr>               <td class="bl"/><td class="b"/><td class="br"/>             </tr>           </tbody>         </table>       </div>     </div>'},loading:function(){k();if(f("#facebox .loading").length==1){return true}e();f("#facebox .content").empty();f("#facebox .body").children().hide().end().append('<div class="loading"><img src="'+f.facebox.settings.loadingImage+'"/></div>');f("#facebox").css({top:h()[1]+(i()/10),left:385.5}).show();f(document).bind("keydown.facebox",function(l){if(l.keyCode==27){f.facebox.close()}return true});f(document).trigger("loading.facebox")},reveal:function(m,l){f(document).trigger("beforeReveal.facebox");if(l){f("#facebox .content").addClass(l)}f("#facebox .content").append(m);f("#facebox .loading").remove();f("#facebox .body").children().fadeIn("normal");f("#facebox").css("left",f(window).width()/2-(f("#facebox table").width()/2));f(document).trigger("reveal.facebox").trigger("afterReveal.facebox")},close:function(){f(document).trigger("close.facebox");return false}});f.fn.facebox=function(l){k(l);function m(){f.facebox.loading(true);var n=this.rel.match(/facebox\[?\.(\w+)\]?/);if(n){n=n[1]}j(this.href,n);return false}return this.click(m)};function k(n){if(f.facebox.settings.inited){return true}else{f.facebox.settings.inited=true}f(document).trigger("init.facebox");d();var l=f.facebox.settings.imageTypes.join("|");f.facebox.settings.imageTypesRegexp=new RegExp("."+l+"$","i");if(n){f.extend(f.facebox.settings,n)}f("body").append(f.facebox.settings.faceboxHtml);var m=[new Image(),new Image()];m[0].src=f.facebox.settings.closeImage;m[1].src=f.facebox.settings.loadingImage;f("#facebox").find(".b:first, .bl, .br, .tl, .tr").each(function(){m.push(new Image());m.slice(-1).src=f(this).css("background-image").replace(/url\((.+)\)/,"$1")});f("#facebox .close").click(f.facebox.close);f("#facebox .close_image").attr("src",f.facebox.settings.closeImage)}function h(){var m,l;if(self.pageYOffset){l=self.pageYOffset;m=self.pageXOffset}else{if(document.documentElement&&document.documentElement.scrollTop){l=document.documentElement.scrollTop;m=document.documentElement.scrollLeft}else{if(document.body){l=document.body.scrollTop;m=document.body.scrollLeft}}}return new Array(m,l)}function i(){var l;if(self.innerHeight){l=self.innerHeight}else{if(document.documentElement&&document.documentElement.clientHeight){l=document.documentElement.clientHeight}else{if(document.body){l=document.body.clientHeight}}}return l}function d(){var l=f.facebox.settings;l.loadingImage=l.loading_image||l.loadingImage;l.closeImage=l.close_image||l.closeImage;l.imageTypes=l.image_types||l.imageTypes;l.faceboxHtml=l.facebox_html||l.faceboxHtml}function j(m,l){if(m.match(/#/)){var n=window.location.href.split("#")[0];var o=m.replace(n,"");f.facebox.reveal(f(o).clone().show(),l)}else{if(m.match(f.facebox.settings.imageTypesRegexp)){c(m,l)}else{g(m,l)}}}function c(m,l){var n=new Image();n.onload=function(){f.facebox.reveal('<div class="image"><img src="'+n.src+'" /></div>',l)};n.src=m}function g(m,l){f.get(m,function(n){f.facebox.reveal(n,l)})}function b(){return f.facebox.settings.overlay==false||f.facebox.settings.opacity===null}function e(){if(b()){return}if(f("facebox_overlay").length==0){f("body").append('<div id="facebox_overlay" class="facebox_hide"></div>')}f("#facebox_overlay").hide().addClass("facebox_overlayBG").css("opacity",f.facebox.settings.opacity).click(function(){f(document).trigger("close.facebox")}).fadeIn(200);return false}function a(){if(b()){return}f("#facebox_overlay").fadeOut(200,function(){f("#facebox_overlay").removeClass("facebox_overlayBG");f("#facebox_overlay").addClass("facebox_hide");f("#facebox_overlay").remove()});return false}f(document).bind("close.facebox",function(){f(document).unbind("keydown.facebox");f("#facebox").fadeOut(function(){f("#facebox .content").removeClass().addClass("content");a();f("#facebox .loading").remove()})})})(jQuery);
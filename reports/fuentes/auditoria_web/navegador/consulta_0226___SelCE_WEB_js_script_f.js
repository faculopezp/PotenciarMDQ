
   	       
$(document).ready(function() {
	
$(".a,.h,.ver,.ver2,.comparativa, .entrar,.btn_entrar").css("cursor","pointer");

/*----------EVOLUCION------*/
$(".no").click(function () { $("select:enabled").attr("disabled","disabled");$("#anoInicial, #anoFinal").removeAttr("disabled");   });
$("#RadioDistrito").click(function () { $("select:enabled").attr("disabled","disabled"); $("#Distrito, #anoInicial, #anoFinal").removeAttr("disabled");   });
$("#RadioRuta").click(function () { $("select:enabled").attr("disabled","disabled"); $("#Ruta, #anoInicial, #anoFinal").removeAttr("disabled");   });
$("#RadioTramo").click(function () { $("select:enabled").attr("disabled","disabled"); $("#Tramo, #anoInicial, #anoFinal").removeAttr("disabled");   });


/*-------------*/

	/*$(".formula").corner("5px");*/
	$("#rangos").change(function () {$(".rango").html(""); var a=$(this).val(); $(".a").hide(); $(".aultimo").show(); $(".rangoultimo").addClass('rango'+a+'Final'); $("input.a").attr("value","");
		for (i=1; i<=a; i++){
			$(".a"+i).show();
			
			
		}
		
		$(".btn_entrar").show()
	});
	
	
	$(".inputText").keyup( function(){  var id=$(this).attr("id"); var input=$(this).val(); var masuno=parseFloat(input);
	
if(isNumeric(input)) $("."+id).html(masuno+1 ) ;
else $("."+id).html("" );

});
    

});

function isNumeric(strString) { 
var strValidChars = "0123456789.-";
 var strChar ; 
   var blnResult = true; 
    if (strString.length == 0) return false; 
      for (i = 0; i < strString.length && blnResult == true; i++)  
      {    strChar = strString.charAt(i);  
       if (strValidChars.indexOf(strChar) == -1) 
       {  blnResult = false;   }  
      }  
      return blnResult;  
      }

function a (a) { setTimeout("moretext()",1000) };

	
/* 

	$(".btn_entrar").css("cursor","cross");
	$.each( ['a'], function(i, e){
  alert( "Item #" + i + ": as" + e );
});

$.each( { name: "John", lang: "JS", esta: "ramo" }, function(i, n){
  alert( "Name: " + i + ", Value: " + n );
});





*/
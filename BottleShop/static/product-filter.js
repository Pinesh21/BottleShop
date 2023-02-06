$(document).ready(function(){
    $(".ajaxLoader").hide();
    $(".filter-checkbox,#priceFilterBtn").on ('click',function(){
        var _filterObj ={};
        var _minPrice = $('#maxPrice').attr('min');
        var _maxPrice = $('#maxPrice').val();
        _filterObj.minPrice = _minPrice;
        _filterObj.maxPrice = _maxPrice;
        console.log(_filterObj.minPrice,_filterObj.maxPrice)
        $(".filter-checkbox").each(function(index,ele){
            var _filterVal =$(this).val();
            var _filterKey =$(this).attr('data-filter');//THis get value set for attribute data-filter in html
            //console.log(_filterVal,_filterKey)
            var x= (document.querySelectorAll('input[data-filter='+_filterKey+']:checked'))//This is to get html element having
            //data-filter matching to filterKey and should be checked
            //console.log(x)
//            for (var i=0; i< x.length; i++){
//                console.log(x[i]);
//                }

            _filterObj[_filterKey]=Array.from(x).map(function(el){
			 	return el.value;
			});
        });
//        console.log(_filterObj)
    $.ajax({
        url:'/filter-data',
        data: _filterObj,
        dataType :'json',
        beforeSend:function(){
        $(".ajaxLoader").show()
        },
        success:function(res){
            console.log(res);
            $("#filteredProducts").html(res.data);
            $(".ajaxLoader").hide()
        }
        });
    });


    //If user enter price outside min and max in price number filter
    //This will alert about it and reset price to min

    $("#maxPrice").on('blur',function(){
        var _min =$(this).attr('min');
        var _max =$(this).attr('max');
        var _value =$(this).val();
        console.log(_value,_min,_max);

        if (_value < parseInt(_min) || _value > parseInt(_max)){
            alert ('Value should be '+_min+'-'+_max);
            $(this).val(_min);
            $(this).focus();
            $("#rangeInput").val(_min);
        }
    });

    });
(function($){
    console.log("---loaded---")

    var nodes = []

    $( "button[data-action]" ).on("click", function() {
        var _action = $(this).data("action")
        switch( _action ){
            case "create_node":
                create_node()
                break
            case "reset_data":
                nodes = []
                break
            case "deploy_nodes":
                deploy_nodes()
                break
            default:
                print("no action")
        }
    });

    function rest( url, type, data={} ) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,
                type: type,
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: resolve,
                error: reject
            })
        });
    }

    function create_node() {
        var node_cost = parseInt( $('input[name="node_cost"]').val() );
        var node_name = $('input[name="node_name"]').val();
        if (node_cost && node_name) {
            nodes.push({
                "cost": node_cost,
                "name": node_name
            });
            console.log(nodes)
        }
    }

    async function deploy_nodes() {
        if( nodes.length > 0 ) {
            rest( "/deploy_nodes", "post", {
                "nodes": nodes
            } ).then(function(res) {
                console.log(res)
            }).catch(function(err) {
                console.log(err)
            }).finally(function() {
                nodes = [] // clear
            })
        }
    }
})(jQuery);
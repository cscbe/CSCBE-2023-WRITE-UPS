var mmm = {}

function dodo()
{
    
    console.log(mmm)
    for(var i = 100000; i<999999; i++){
        res = mmm.vault.a(i + "", "de287e29a4a38788ba96136d6c2f21d0")

        if(i % 100000 == 0){
            console.log(i)
        }
        if(res)
        {
            console.log("Code: " + i)
            return;
        }
    }
}

function test(){
    Java.perform(function(){
        Java.enumerateClassLoaders({
            onMatch: function(loader){
                Java.classFactory.loader = loader;
                var TestClass;

                try{
                    var VaultClass = Java.use("be.dauntless.twofa.Vault");
                    var v = VaultClass.$new();
                    console.log("a = \"" + v._a.value + "\"")
                    console.log("c = \"" + v.c.value + "\"")
                    console.log("b = \"" + v.b.value + "\"")
                    return;

                }catch(error){
                    console.log(error)
                    
                }
            },
            onComplete: function(){

            }
        });

    })

}
setTimeout(test, 2000)


        var keyList = "abcdefghijklmnopqrstuvwxyz123456789!@#$%^&*";
        var tmp = '';

        function generatePass(plength) {
            tmp='';
            for(i = 0; i < plength; ++i) {
                tmp+=keyList.charAt(Math.floor(Math.random()*keyList.length));
            }
            console.log(tmp);
            return tmp;
        }


        function getPassword(enterLength) {
            document.passGen.output.value = generatePass(enterLength);
        }

        const btn = document.getElementById("getPass");

        if (btn) {
        btn.addEventListener("click", function() {
            getPassword(document.passGen.length.value);
        });
        }
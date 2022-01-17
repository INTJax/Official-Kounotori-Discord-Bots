const fetch = require('node-fetch');
const ethers = require("ethers");
var fs = require('fs');
let Count = 0;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

async function main() {

    // specifying the deployed contract address, etherscan apikey, private key, ETH node address and output file location
    const contractaddress = "0x616ef40D55C0D2c506f4d6873Bda8090b79BF8fC";
    const apikey = (fs.readFileSync(".\\Etherscan.txt"));
    const privatekey = (fs.readFileSync(".\\Wallet.txt"));
    const node = encodeURI(fs.readFileSync(".\\Node.txt"));
    const OutPath = "\\\\domcon_1\\KTO_Data";
    const Regex = new RegExp('\\d{1,3},\\d{1,3},\\d{1,3}');

    while(1) {
        try {
            // make an API call to the ABIs endpoint
            let response = await fetch('https://api.etherscan.io/api?module=contract&action=getabi&address=' + contractaddress + '&apikey=' + apikey);
            let data = await response.json();
            
            // get JSON formatted contract abi and print to console
            let abi = data.result;
            //console.log(abi);

            // creating a new Provider, and passing in our node URL
            let provider = new ethers.providers.WebSocketProvider(node);

            // initiating a new Wallet, passing in our private key to sign transactions
            let wallet = new ethers.Wallet(privatekey, provider);

            // print the wallet address
            //console.log("Using wallet address " + wallet.address);

            // initiating a new Contract
            let contract = new ethers.Contract(contractaddress, abi, wallet);

            // retrieve current buy tax rate
            let GetBuyTaxes = await contract._buyTaxes();
            let BuyTaxes = GetBuyTaxes.toString()
            //console.log("Current Buy Taxes are " + BuyTaxes);

            // retrieve current sell tax rate
            let GetSellTaxes = await contract._sellTaxes();
            let SellTaxes = GetSellTaxes.toString()
            //console.log("Current Sell Taxes are " + SellTaxes);

            // retrieve current transfer tax rate
            let GetTransferTaxes = await contract._transferTaxes();
            let TransferTaxes = GetTransferTaxes.toString()
            //console.log("Current Transfer Taxes are " + TransferTaxes);

            // if the tax numbers are returned as expected, calculate the reflect rate and marketing tax
            if((Regex.test(BuyTaxes)) && (Regex.test(SellTaxes)) && (Regex.test(TransferTaxes))) {
                let BuyArray = BuyTaxes.split(",");
                let SellArray = SellTaxes.split(",");
                let TferArray = TransferTaxes.split(",");

                let BuyReflect = (BuyArray[0]/100)
                let BuyLTax = (BuyArray[1]/100)
                let BuyMTax = (BuyArray[2]/100)

                let SellReflect = (SellArray[0]/100)
                let SellLTax = (SellArray[1]/100)
                let SellMTax = (SellArray[2]/100)

                let TferReflect = (TferArray[0]/100)
                let TferLTax = (TferArray[1]/100)
                let TferMTax = (TferArray[2]/100)

                let BuyTax = (BuyReflect + BuyLTax + BuyMTax)
                let SellTax = (SellReflect + SellLTax + SellMTax)
                let TferTax = (TferReflect + TferLTax + TferMTax)

                // write out main tax data
                fs.writeFile(OutPath + "\\KTO_Tax.txt", BuyTax + "% | " + SellTax + "% | " + TferTax + "%" , function (err) {
                    if (err) throw err;
                });

                // write out additional tax data
                fs.writeFile(OutPath + "\\Tax_Details\\BuyReflect.txt", BuyReflect + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\BuyLTax.txt", BuyLTax + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\BuyMTax.txt", BuyMTax + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\SellReflect.txt", SellReflect + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\SellLTax.txt", SellLTax + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\SellMTax.txt", SellMTax + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\TferReflect.txt", TferReflect + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\TferLTax.txt", TferLTax + "%" , function (err) {
                    if (err) throw err;
                });
                fs.writeFile(OutPath + "\\Tax_Details\\TferMTax.txt", TferMTax + "%" , function (err) {
                    if (err) throw err;
                });
            }
            else {
                console.log("ERROR: Taxes are not correct!")
            }
            await sleep(60000);
            //Count += 1
            //console.log("Count = " + Count.toString())
        }
        catch(e) {
            console.log(e);
        }
    }
    console.log("ERROR: Script ended early!")
}

main();

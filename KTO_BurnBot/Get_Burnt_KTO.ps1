
#Functional Variables
$Delay = 60
$Root = "C:\Delivery\Scripts\KTO_BurnBot"
$OutputFile = "$Root\BurntKTO.txt"
$Errors = 0

#Token Variables
$Contract = "0x616ef40D55C0D2c506f4d6873Bda8090b79BF8fC"
$Wallet = "0x000000000000000000000000000000000000dead"
$APIKey = "P5R698PKNYATT3Q58GVKQCQGBRKDPZC8BF"
$URL = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=$($Contract)&address=$($Wallet)&tag=latest&apikey=$($APIKey)"

#Email Variables
$EmailFrom = "alerts@schrader.home"
$EmailSubject = "KTO BURN BOT ERROR"
$EmailTo = "intjaxau@gmail.com"
$EmailServer = "JS-HOST"

#Email Credentials
$EmailUser = "alerts@schrader.home"
$EmailPassFile = "$Root\EmailPass.txt"
[securestring]$EmailPass = ConvertTo-SecureString (Get-Content $EmailPassFile) -AsPlainText -Force
[pscredential]$EmailCredentials = (New-Object System.Management.Automation.PSCredential ($EmailUser, $EmailPass))

#Update holders every 60 seconds and send email if there is an error
While($true) {
    $Response = Invoke-WebRequest $URL
    if($Response.StatusCode -eq 200) {
        [double]$Number = ((($Response | ConvertFrom-Json).result).substring(0,15))
        $BurntKTO = ('{0:N0}' -f $Number)
        $BurntKTO | Out-File $OutputFile -Encoding default -NoNewline -Force
        $Errors = 0
    }
    else {
        $Errors++
        if($Errors -eq 3) {
            Send-MailMessage -From $EmailFrom -Subject $EmailSubject -To $EmailTo -SmtpServer $EmailServer -Credential $EmailCredentials
        }
    }
    Start-Sleep -Seconds $Delay
}

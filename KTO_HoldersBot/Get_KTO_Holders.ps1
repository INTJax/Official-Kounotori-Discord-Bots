
#Functional Variables
$Delay = 60
$OutputFile = "C:\Delivery\Scripts\KTO_HoldersBot\Holders.txt"
$Errors = 0

#Email Variables
$EmailFrom = "alerts@schrader.home"
$EmailSubject = "KTO HOLDER BOT ERROR"
$EmailTo = "intjaxau@gmail.com"
$EmailServer = "JS-HOST"

#Email Credentials
$EmailUser = "alerts@schrader.home"
$EmailPassFile = "C:\Delivery\Scripts\KTO_HoldersBot\EmailPass.txt"
[securestring]$EmailPass = ConvertTo-SecureString (Get-Content $EmailPassFile) -AsPlainText -Force
[pscredential]$EmailCredentials = (New-Object System.Management.Automation.PSCredential ($EmailUser, $EmailPass))

#Update holders every 60 seconds and send email if there is an error
While($true) {
    if($Matches -gt 0) {
        $Matches.Clear()
    }
    $Result = ((Invoke-WebRequest "https://etherscan.io/token/0x616ef40D55C0D2c506f4d6873Bda8090b79BF8fC").Content -match 'number of holders ((,)*(\d)+)+')
    if($Result -eq $true) {
        $Holders = ($Matches[0].Substring(18))
        $Holders | Out-File $OutputFile -Encoding default -NoNewline -Force
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

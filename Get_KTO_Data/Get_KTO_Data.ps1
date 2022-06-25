
#Functional Variables
$Delay = 60
$Root = "C:\Delivery\Scripts\Get_KTO_Data"
$OutRoot = "\\DOMCON_1\KTO_Data"
$Errors = 0

#Token Variables
[double]$TotalSupply = 1000000000000000
$KTOContract = "0x616ef40D55C0D2c506f4d6873Bda8090b79BF8fC"
$BurnWallet = "0x000000000000000000000000000000000000dead"
$EScanAPIKey = (Get-Content "$Root\Etherscan.txt")
$Token = "kounotori"
$CGURL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=$($Token)&order=market_cap_desc&per_page=100&page=1&sparkline=false"
$BurnURL = "https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress=$($KTOContract)&address=$($BurnWallet)&tag=latest&apikey=$($EScanAPIKey)"
$HoldersURL = "https://etherscan.io/token/$($KTOContract)"

#Email Variables - FILL THESE IN
$EmailFrom = "FROM_ADDRESS"
$EmailSubject = "KTO DATA FETCH ERROR"
$EmailTo = "TO_ADDRESS"
$EmailServer = "SMTP_SERVER"

#Email Credentials
$EmailUser = "EMAIL" # FILL THIS IN
$EmailPassFile = "$Root\Email.txt"
[securestring]$EmailPass = ConvertTo-SecureString (Get-Content $EmailPassFile) -AsPlainText -Force
[pscredential]$EmailCredentials = (New-Object System.Management.Automation.PSCredential ($EmailUser, $EmailPass))

#Update data every 60 seconds and send email if there is an error
While($true) {
    #Get KTO Price & Volume
    $CGResponse = Invoke-WebRequest $CGURL -UseBasicParsing
    if($CGResponse.StatusCode -eq 200) {
        $CGData = ((Invoke-WebRequest $CGURL).content | ConvertFrom-Json)
        [decimal]$Price = (($CGData.current_price) -as [decimal])
        $Price | Out-File "$OutRoot\KTO_Price.txt" -Encoding default -NoNewline -Force
        $Temp0 = ($CGData.total_volume)
        $Volume = ('{0:N0}' -f $Temp0)
        $Volume | Out-File "$OutRoot\KTO_Volume.txt" -Encoding default -NoNewline -Force
        #Get number of KTO in dead wallet
        $BurnResponse = Invoke-WebRequest $BurnURL
        if($BurnResponse.StatusCode -eq 200) {
            [double]$Temp1 = ((($BurnResponse | ConvertFrom-Json).result).substring(0,15))
            $BurntKTO = ('{0:N0}' -f $Temp1)
            $BurntKTO | Out-File "$OutRoot\KTO_Burnt.txt" -Encoding default -NoNewline -Force
            #Calculate circulating supply
            $Temp2 = ($TotalSupply-$BurntKTO)
            $CirculatingSupply = ('{0:N0}' -f $Temp2)
            $CirculatingSupply | Out-File "$OutRoot\KTO_Supply.txt" -Encoding default -NoNewline -Force
            #Calculate market cap
            $Temp3 = ($Temp2*$Price)
            $MarketCap = ('{0:N0}' -f $Temp3)
            $MarketCap | Out-File "$OutRoot\KTO_MCap.txt" -Encoding default -NoNewline -Force
            #Get number of KTO holders
            if($Matches.Count -gt 0) {
                $Matches.Clear()
            }
            $HoldersResponse = ((Invoke-WebRequest $HoldersURL).Content -match 'number of holders ((,)*(\d)+)+')
            if($HoldersResponse -eq $true) {
                $Holders = ($Matches[0].Substring(18))
                $Holders | Out-File "$OutRoot\KTO_Holders.txt" -Encoding default -NoNewline -Force
                $Errors = 0
            }
            else {
                $Errors++
                if($Errors -eq 3) {
                    Send-MailMessage -From $EmailFrom -Subject $EmailSubject -To $EmailTo -SmtpServer $EmailServer -Credential $EmailCredentials
                }
            }
        }
        else {
            $Errors++
            if($Errors -eq 3) {
                Send-MailMessage -From $EmailFrom -Subject $EmailSubject -To $EmailTo -SmtpServer $EmailServer -Credential $EmailCredentials
            }
        }
    }      
    else {
        $Errors++
        if($Errors -eq 3) {
            Send-MailMessage -From $EmailFrom -Subject $EmailSubject -To $EmailTo -SmtpServer $EmailServer -Credential $EmailCredentials
        }
    }
    Start-Sleep -Seconds $Delay
}

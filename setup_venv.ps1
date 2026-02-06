# This script sets up a Python virtual environment in the parent directory and installs dependencies from requirements.txt
$venvName = ".venv"
$venvPath = Join-Path -Path $PSScriptRoot -ChildPath $venvName
$requirementsPath = Join-Path -Path $PSScriptRoot -ChildPath "requirements.txt"
$lastInstallPath = Join-Path -Path $venvPath -ChildPath ".last_requirements_install"

function Activate-VirtualEnvironment
{
    Write-Host "Activating Python virtual environment at $($venvPath)"
    
    $activateScript = Join-Path -Path $venvPath -ChildPath "Scripts\Activate.ps1"
    
    if ( Test-Path -Path $activateScript ) {
        & $activateScript
        Write-Host "Virtual environment activated."
    } else {
        Write-Error "Activation script not found at $($activateScript)"
        exit 1
    }
}

function Install-Requirements
{
    param(
        [string]$Reason = "Installing dependencies"
    )
    
    if ( Test-Path $requirementsPath ) {
        Write-Host "$Reason from requirements.txt..." -ForegroundColor Yellow
        
        # Upgrade pip to the latest version
        Write-Host "Upgrading pip to the latest version..."
        python -m pip install --upgrade pip
        
        # Install/update dependencies
        pip install -r $requirementsPath
        
        # Record the timestamp of this installation
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Set-Content -Path $lastInstallPath -Value $timestamp
        Write-Host "Dependencies installation completed at $timestamp" -ForegroundColor Green
    } else {
        Write-Warning "requirements.txt not found at $requirementsPath"
    }
}

function Test-RequirementsNeedUpdate
{
    # If requirements.txt doesn't exist, no need to update
    if ( -not (Test-Path $requirementsPath) ) {
        return $false
    }
    
    # If we've never installed requirements, we need to install
    if ( -not (Test-Path $lastInstallPath) ) {
        Write-Host "No previous requirements installation found." -ForegroundColor Yellow
        return $true
    }
    
    # Get the last modification time of requirements.txt
    $requirementsModified = (Get-Item $requirementsPath).LastWriteTime
    
    # Get the timestamp of last installation
    $lastInstallTime = Get-Content $lastInstallPath | Get-Date
    
    # Compare timestamps
    if ( $requirementsModified -gt $lastInstallTime ) {
        Write-Host "requirements.txt has been modified since last installation." -ForegroundColor Yellow
        Write-Host "  Requirements file: $($requirementsModified)"
        Write-Host "  Last installation: $($lastInstallTime)"
        return $true
    }
    
    Write-Host "Requirements are up to date (last installed: $lastInstallTime)" -ForegroundColor Green
    return $false
}

function Initialize-PythonVEnv
{
    Write-Host "Create python virtual environment in $($venvPath)"

    Push-Location $PSScriptRoot

    python -m venv $venvName

    Pop-Location

    if ( Test-Path -Path $venvPath ) {
        Write-Host "Python virtual environment '$($venvName)' has been created successfully." -ForegroundColor Green

        Activate-VirtualEnvironment

        # Install initial requirements
        Install-Requirements -Reason "Installing initial dependencies"

        Write-Host "Virtual environment setup complete."
    } else {
        throw "Failed to create the Python virtual environment."
    }
}

function Test-PythonVirtualEnvironment
{
    Write-Host "Check if the python virtual environment is setup..."

    if ( $false -eq ( Test-Path -Path $venvPath ) ) {
        Write-Warning "No Python virtual environment found in the working directory at $($venvPath)."
        
        Initialize-PythonVEnv
    } else {
        Write-Host "Python virtual environment found at $venvPath" -ForegroundColor Green
        Activate-VirtualEnvironment
        
        # Check if requirements need to be updated
        if ( Test-RequirementsNeedUpdate ) {
            Install-Requirements -Reason "Updating dependencies"
        }
    }
}

Test-PythonVirtualEnvironment
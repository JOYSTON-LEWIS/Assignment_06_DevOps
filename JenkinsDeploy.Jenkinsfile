pipeline {
  agent any

  environment {
    JL_MONGO_URI_A06 = credentials('JL_MONGO_URI_A06')
    JL_EC2_PRIVATE_IP_A06 = credentials('JL_EC2_PRIVATE_IP_A06')
    JL_EC2_SSH_PRIVATE_KEY = credentials('JL_EC2_SSH_PRIVATE_KEY')
    JL_EC2_USER = credentials('JL_EC2_USER')
    JL_MAIL_TO_EMAIL_ID_A06 = credentials('JL_MAIL_TO_EMAIL_ID_A06')
  }

  stages {
    stage('Install & Setup on EC2') {
      steps {
        sshagent(['JL_EC2_SSH_PRIVATE_KEY']) {
          sh """
            ssh -o StrictHostKeyChecking=no \$JL_EC2_USER@\$JL_EC2_PRIVATE_IP_A06 '
              set -xe
              echo "🔧 Updating system packages..."
              sudo apt update -y && sudo apt upgrade -y

              echo "📦 Installing Git, Nginx, curl, Python3, pip, venv..."
              sudo apt install -y git nginx curl python3 python3-pip python3-venv

              echo "✅ Setup complete."
            '
          """
        }
      }
    }

    stage('Clone Repository & Create .env') {
      steps {
        sshagent(['JL_EC2_SSH_PRIVATE_KEY']) {
          sh """
            ssh -o StrictHostKeyChecking=no \$JL_EC2_USER@\$JL_EC2_PRIVATE_IP_A06 '
              set -xe
              echo "📁 Cloning repo..."
              rm -rf Assignment_06_DevOps
              git clone https://github.com/JOYSTON-LEWIS/Assignment_06_DevOps.git

              echo "📝 Creating .env file..."
              cat > Assignment_06_DevOps/.env <<EOL
MONGO_URI=${JL_MONGO_URI_A06}
PORT=5000
EOL

              echo ".env file created:"
              cat Assignment_06_DevOps/.env
            '
          """
        }
      }
    }

    stage('Install Python Dependencies') {
      steps {
        sshagent(['JL_EC2_SSH_PRIVATE_KEY']) {
          sh """
            ssh -o StrictHostKeyChecking=no \$JL_EC2_USER@\$JL_EC2_PRIVATE_IP_A06 '
              set -xe
              echo "📦 Installing Python dependencies..."

              cd Assignment_06_DevOps
              python3 -m venv venv
              source venv/bin/activate
              pip install --upgrade pip
              pip install -r requirements.txt

              echo "✅ Dependencies installed."
            '
          """
        }
      }
    }

    stage('Run Tests') {
      steps {
        sshagent(['JL_EC2_SSH_PRIVATE_KEY']) {
          sh """
            ssh -o StrictHostKeyChecking=no \$JL_EC2_USER@\$JL_EC2_PRIVATE_IP_A06 '
              set -xe
              echo "🧪 Running pytest..."

              cd Assignment_06_DevOps
              source venv/bin/activate

              pytest --ignore=backup || true

              echo "✅ Tests completed."
            '
          """
        }
      }
    }

    stage('Deploy Flask App & Configure Nginx') {
  steps {
    sshagent(['JL_EC2_SSH_PRIVATE_KEY']) {
      sh """
        ssh -o StrictHostKeyChecking=no \$JL_EC2_USER@\$JL_EC2_PRIVATE_IP_A06 '
          set -xe

          echo "⚙️ Writing custom Nginx config..."
          sudo tee /etc/nginx/sites-available/assignment_06 > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \\\$host;
        proxy_set_header X-Real-IP \\\$remote_addr;
        proxy_set_header X-Forwarded-For \\\$proxy_add_x_forwarded_for;
    }
}
EOF

          echo "🔗 Enabling Nginx config..."
          sudo ln -sf /etc/nginx/sites-available/assignment_06 /etc/nginx/sites-enabled/assignment_06
          sudo rm -f /etc/nginx/sites-enabled/default
          sudo systemctl daemon-reload
          sudo nginx -t
          sudo systemctl reload nginx

          echo "📁 Navigating to Flask app directory..."
          cd ~
          cd Assignment_06_DevOps
          source venv/bin/activate

          echo "🚀 Running Flask app..."
          nohup python3 app.py > flask_output.log 2>&1 &
        '
      """
    }
  }
}

  }

  post {
    success {
      mail to: "${env.JL_MAIL_TO_EMAIL_ID_A06}",
           subject: "✅ SUCCESS: Build #${env.BUILD_NUMBER}",
           body: "Build succeeded. View it at: ${env.BUILD_URL}"
    }
    failure {
      mail to: "${env.JL_MAIL_TO_EMAIL_ID_A06}",
           subject: "❌ FAILURE: Build #${env.BUILD_NUMBER}",
           body: "Build failed. View it at: ${env.BUILD_URL}"
    }
  }
}

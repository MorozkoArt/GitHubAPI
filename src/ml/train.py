import torch
import pandas as pd
import torch.nn as nn
from sklearn.model_selection import train_test_split
from src.ml.GenerationUsers.С_generation_fake_users import GitHubUserGenerator
from C_dataset import GitHubDataset
from pathlib import Path
from torch.utils.data import DataLoader
from C_model import GitHubModel
import torch.optim as optim
from M_education import evaluate, train_epoch



def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    base_dir = Path(__file__).parents[2]
    path = base_dir / "data" / "training.csv"

    if not Path(path).exists():
        generator = GitHubUserGenerator()
        dff = generator.generate_users()
        generator.save_to_csv(dff, path)

    df = pd.read_csv(path)

    X = df.drop(columns=["followers", "following", "hireable", "repos", "created_update",
        "plan", "blog", "company", "org", "languages", "forks", "stars", "avg_cont",
        "avg_a_days", "frequencyCommits", "inDayCommits", "countCommits", "avg_views",
        "forks_r", "stars_r", "cont_count", "active_days_r", "commits_repo",
        "frequency_repo", "inDay_repo", "addLine", "delLine", "count_views"])

    y = df[["followers_s", "following_s", "hireable_s", "repos_s", "created_update_s",
        "plan_s", "blog_s", "company_s", "org_s", "langs_s", "forks_s", "stars_s",
        "freq_commits_s", "avg_cont_s", "avg_a_days_s", "in_day_commits_s",
        "count_commits_s", "avg_views_s",
        "forks_r_s", "stars_r_s", "contributors_s", "active_days_r_s", "commits_repo_s",
        "in_day_repo_s", "frequency_repo_s", "add_line_s", "del_line_s",
        "count_views_s"]]

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    train_dataset = GitHubDataset(X_train, y_train)
    val_dataset = GitHubDataset(X_val, y_val)
    test_dataset = GitHubDataset(X_test, y_test)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=64)
    test_loader = DataLoader(test_dataset, batch_size=64)


    model = GitHubModel(input_size=X_train.shape[1],
                        output_size=y_train.shape[1]).to(device)

    criterion = nn.SmoothL1Loss()
    optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=3)
    best_loss = float('inf')

    for epoch in range(200):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss, val_mae, val_r2 = evaluate(model, val_loader, criterion, device)
        scheduler.step(val_loss)

        print(f"Epoch {epoch + 1}:")
        print(f"  Train Loss: {train_loss:.4f}")
        print(f"  Val Loss: {val_loss:.4f}, MAE: {val_mae:.4f}, R2: {val_r2:.4f}")

        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), "best_model.pth")
            print("  Saved best model!")

    print("\nTesting best model...")
    model.load_state_dict(torch.load("best_model.pth"))
    test_loss, test_mae, test_r2 = evaluate(model, test_loader, criterion, device)
    print(f"Test Loss: {test_loss:.4f}, MAE: {test_mae:.4f}, R2: {test_r2:.4f}")

if __name__ == '__main__':
    main()
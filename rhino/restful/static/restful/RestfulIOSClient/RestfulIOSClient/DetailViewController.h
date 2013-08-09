//
//  DetailViewController.h
//  RestfulIOSClient
//
//  Created by 孔 令开 on 13-5-14.
//  Copyright (c) 2013年 Egibbon. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface DetailViewController : UIViewController <UITableViewDataSource, UITableViewDelegate, UIAlertViewDelegate>

@property (strong, nonatomic) id detailItem;

@property (strong, nonatomic) IBOutlet UILabel *detailDescriptionLabel;
@property (strong, nonatomic) IBOutlet UITableView *tableView;

- (IBAction)doTest:(id)sender;

@end
